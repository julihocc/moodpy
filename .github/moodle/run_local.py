"""Run Moodle's importer and grader in disposable, isolated Docker containers.

Named volumes and stdin file transfers also work with Windows docker.exe from WSL.
Requires generated core/migrated banks with independent expectations.json files.
"""

import argparse
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import subprocess
import tarfile
import time
import uuid


VERSIONS = {
    "4.5": "MOODLE_405_STABLE",
    "5.0": "MOODLE_500_STABLE",
    "5.1": "MOODLE_501_STABLE",
    "5.2": "MOODLE_502_STABLE",
}
PHP_IMAGE = "moodlehq/moodle-php-apache:8.3"


def fixture_archive(core, migrated):
    buffer = io.BytesIO()
    plugin = Path(__file__).parent / "local_moodpycompat"
    with tarfile.open(fileobj=buffer, mode="w") as archive:
        for source in sorted(plugin.rglob("*")):
            if source.is_file():
                archive.add(source, arcname=str(source.relative_to(plugin)))
        for name, bank in (("core", core), ("migrated", migrated)):
            for filename in ("bank.xml", "manifest.json", "expectations.json"):
                archive.add(
                    bank / filename, arcname="tests/fixtures/" + name + "/" + filename
                )
    return buffer.getvalue()


def test_version(docker, version, fixtures, output):
    output.mkdir(parents=True, exist_ok=False)
    prefix = "moodpycompat-" + uuid.uuid4().hex[:12]
    network, volume = prefix + "-net", prefix + "-source"
    database, web, composer = prefix + "-db", prefix + "-web", prefix + "-composer"
    result = {
        "requested_version": version,
        "branch": VERSIONS[version],
        "status": "failed",
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    started = time.monotonic()
    logpath = output / "run.log"

    with logpath.open("wb") as log:

        def run(*args, data=None, timeout=900, check=True):
            log.write(("\n$ docker " + " ".join(args) + "\n").encode())
            log.flush()
            return subprocess.run(
                [docker, *args],
                input=data,
                stdout=log,
                stderr=subprocess.STDOUT,
                check=check,
                timeout=timeout,
            )

        def phase(name):
            result["phase"] = name
            print("Moodle " + version + ": " + name, flush=True)

        try:
            phase("create isolated network and source volume")
            run("network", "create", network)
            run("volume", "create", volume)
            phase("checkout Moodle and install PHPUnit dependencies")
            setup = (
                "git clone --depth 1 --branch "
                + VERSIONS[version]
                + " https://github.com/moodle/moodle.git /app; "
                "git clone --depth 1 https://github.com/moodlehq/moodle-docker.git /app/.moodpy-docker; "
                "cp .moodpy-docker/config.docker-template.php config.php; "
                "git rev-parse HEAD > moodpy-moodle-compat-revision.txt; "
                "git -C .moodpy-docker rev-parse HEAD >> moodpy-moodle-compat-revision.txt; "
                "composer install --no-interaction --prefer-dist --no-progress --ignore-platform-reqs"
            )
            run(
                "run",
                "--rm",
                "--name",
                composer,
                "--volume",
                volume + ":/app",
                "--workdir",
                "/app",
                "composer:2",
                "sh",
                "-ec",
                setup,
            )
            phase("start PostgreSQL 16 and Moodle PHP 8.3")
            run(
                "run",
                "-d",
                "--name",
                database,
                "--network",
                network,
                "--network-alias",
                "db",
                "-e",
                "POSTGRES_USER=moodle",
                "-e",
                "POSTGRES_PASSWORD=moodpy-test-only",
                "-e",
                "POSTGRES_DB=moodle",
                "postgres:16",
            )
            run(
                "run",
                "-d",
                "--name",
                web,
                "--network",
                network,
                "--volume",
                volume + ":/var/www/html",
                "--workdir",
                "/var/www/html",
                "-e",
                "MOODLE_DOCKER_RUNNING=1",
                "-e",
                "MOODLE_DOCKER_DBTYPE=pgsql",
                "-e",
                "MOODLE_DOCKER_DBNAME=moodle",
                "-e",
                "MOODLE_DOCKER_DBUSER=moodle",
                "-e",
                "MOODLE_DOCKER_DBPASS=moodpy-test-only",
                PHP_IMAGE,
            )
            run(
                "exec",
                "-i",
                web,
                "sh",
                "-ec",
                "if [ -d public ]; then prefix=public/; else prefix=; fi; "
                'mkdir -p "${prefix}local/moodpycompat"; '
                'tar -xf - -C "${prefix}local/moodpycompat"',
                data=fixtures,
            )
            for attempt in range(60):
                if (
                    run(
                        "exec",
                        database,
                        "pg_isready",
                        "-h",
                        "127.0.0.1",
                        "-U",
                        "moodle",
                        timeout=10,
                        check=False,
                    ).returncode
                    == 0
                ):
                    break
                time.sleep(1)
            else:
                raise RuntimeError("PostgreSQL did not become ready")
            phase("install disposable site and initialize PHPUnit")
            install = r"""
                if [ -d public ]; then prefix=public/; else prefix=; fi
                php -l "${prefix}local/moodpycompat/tests/import_test.php"
                php -r 'define("MOODLE_INTERNAL", true);
                  define("MATURITY_ALPHA", 50); define("MATURITY_BETA", 100);
                  define("MATURITY_RC", 150); define("MATURITY_STABLE", 200);
                  require (is_dir("public") ? "public/" : "") . "version.php";
                  echo json_encode(["release" => $release, "branch" => $branch,
                    "version" => $version, "php" => PHP_VERSION], JSON_PRETTY_PRINT);' \
                  > moodpy-moodle-compat-runtime.json
                php admin/cli/install_database.php --agree-license \
                  --fullname="MoodPy compatibility" --shortname="moodpycompat" \
                  --summary="Disposable local test site" \
                  --adminpass="test" --adminemail="admin@example.com"
                php "${prefix}admin/tool/phpunit/cli/init.php"
            """
            run("exec", web, "sh", "-ec", install)
            phase("import both banks and grade independent answers")
            grading = r"""
                if [ -d public ]; then prefix=public/; else prefix=; fi
                if [ -f phpunit.xml ]; then config=phpunit.xml; else config=public/phpunit.xml; fi
                vendor/bin/phpunit --configuration="$config" \
                  --log-junit=moodpy-moodle-compat-junit.xml \
                  "${prefix}local/moodpycompat/tests/import_test.php"
            """
            run("exec", web, "sh", "-ec", grading)
            result["status"] = "passed"
        except (subprocess.SubprocessError, OSError, RuntimeError) as error:
            result["failed_phase"] = result["phase"]
            result["error"] = str(error)
            print("Moodle " + version + ": FAILED; see " + str(logpath), flush=True)
        finally:
            # Copy evidence via stdout: no host bind paths or WSL integration needed.
            for filename in (
                "moodpy-moodle-compat-runtime.json",
                "moodpy-moodle-compat-revision.txt",
                "moodpy-moodle-compat-junit.xml",
            ):
                try:
                    with (output / filename).open("wb") as report:
                        copied = subprocess.run(
                            [docker, "exec", web, "cat", "/var/www/html/" + filename],
                            stdout=report,
                            stderr=log,
                            timeout=30,
                        )
                    if copied.returncode:
                        result.setdefault("report_errors", []).append(
                            "Could not copy " + filename
                        )
                        (output / filename).unlink()
                except (subprocess.SubprocessError, OSError) as error:
                    result.setdefault("report_errors", []).append(str(error))
                    log.write(
                        (
                            "Unable to copy " + filename + ": " + str(error) + "\n"
                        ).encode()
                    )
                    if (output / filename).exists():
                        (output / filename).unlink()
            result["completed_phase"] = result["phase"]
            phase("remove only this run's containers, volume and network")
            cleanup = [("rm", "-f", "-v", name) for name in (composer, web, database)]
            cleanup += [("volume", "rm", volume), ("network", "rm", network)]
            for command in cleanup:
                try:
                    cleaned = run(*command, timeout=60, check=False)
                    if cleaned.returncode:
                        result.setdefault("cleanup_errors", []).append(
                            "docker "
                            + " ".join(command)
                            + " failed with exit "
                            + str(cleaned.returncode)
                        )
                except (subprocess.SubprocessError, OSError) as error:
                    result.setdefault("cleanup_errors", []).append(str(error))
            result["duration_seconds"] = round(time.monotonic() - started, 2)
            (output / "result.json").write_text(
                json.dumps(result, indent=2) + "\n", encoding="utf-8"
            )
    print("Moodle " + version + ": " + result["status"].upper(), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--docker", default="docker", help="Docker CLI path; docker.exe is supported"
    )
    parser.add_argument(
        "--versions", nargs="+", choices=VERSIONS, default=list(VERSIONS)
    )
    parser.add_argument("--core-bank", type=Path, required=True)
    parser.add_argument("--migrated-bank", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="New report directory (never overwritten)",
    )
    args = parser.parse_args()
    if len(set(args.versions)) != len(args.versions):
        parser.error("--versions must not contain duplicate branches")
    fixtures = fixture_archive(args.core_bank, args.migrated_bank)
    args.output.mkdir(parents=True, exist_ok=False)
    for name, bank in (("core", args.core_bank), ("migrated", args.migrated_bank)):
        target = args.output / name
        target.mkdir()
        for filename in ("bank.xml", "manifest.json", "expectations.json"):
            (target / filename).write_bytes((bank / filename).read_bytes())
    results = [
        test_version(args.docker, version, fixtures, args.output / version)
        for version in args.versions
    ]
    (args.output / "results.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8"
    )
    return int(
        any(
            result["status"] != "passed"
            or result.get("report_errors")
            or result.get("cleanup_errors")
            for result in results
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
