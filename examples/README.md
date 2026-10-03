# MoodPy examples

The supported agent workflow starts at [agent_workflow/author_bank.py](agent_workflow/author_bank.py)
and [its brief](agent_workflow/brief.md). Follow the
[authoring guide](../docs/authoring-guide.md) and [verified recipe catalog](../docs/verified-recipes.md).

Run after installing the matching repository package:

```bash
python examples/agent_workflow/author_bank.py --seed 42 --samples 2 --output artifacts/sample
```

The scripts in [legacy/](legacy/README.md) are historical references requiring verification before
reuse. Some retain Sage syntax, Python 2 constructs, missing dependencies, or
migration TODOs. Their existence does not certify generation or mathematical correctness.
Use the verified catalog when an agent needs a dependable starting point.
