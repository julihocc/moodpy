#!/usr/bin/env python3
"""
MoodPy Legacy Generator Migration Utility

This script helps migrate percent-format Python generators from the legacy
generators/ directory into the modern MoodPy v3.0.0 package structure.

Usage:
    python migrate_generator.py <generator_file.py> <subject_area>
    
Example:
    python migrate_generator.py "generators/MOODPY MAN 101 PRECIO DE EQUILIBRIO.py" economics
"""

import os
import re
import sys
from pathlib import Path


class GeneratorMigrator:
    def __init__(self):
        self.subjects_dir = Path("src/moodpy/subjects")
        self.generators_dir = Path("generators")
        
    def analyze_generator(self, filepath):
        """Analyze a generator file and extract metadata."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract basic information
        info = {
            'filepath': filepath,
            'filename': Path(filepath).name,
            'has_moodpy_import': 'import moodpy' in content or 'from moodpy' in content,
            'has_numpy': 'import numpy' in content,
            'has_sage': 'sage' in content.lower(),
            'has_html': 'html(' in content,
            'cell_count': content.count('# %%'),
            'functions': re.findall(r'def\s+(\w+)', content),
            'variables': re.findall(r'(\w+)\s*=.*(?:random|np\.random)', content)
        }
        
        # Try to extract title/label
        label_match = re.search(r'label\s*=\s*["\']([^"\']+)["\']', content)
        if label_match:
            info['title'] = label_match.group(1)
        else:
            # Use filename as fallback
            info['title'] = Path(filepath).stem
            
        return info
        
    def convert_to_module(self, filepath, subject_area):
        """Convert a percent-format generator to a modern module."""
        info = self.analyze_generator(filepath)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Remove Jupyter metadata
        lines = content.split('\n')
        filtered_lines = []
        in_jupyter_header = False
        
        for line in lines:
            if line.strip() == '# ---' and not in_jupyter_header:
                in_jupyter_header = True
                continue
            elif line.strip() == '# ---' and in_jupyter_header:
                in_jupyter_header = False
                continue
            elif in_jupyter_header:
                continue
            else:
                filtered_lines.append(line)
                
        # Clean content
        cleaned_content = '\n'.join(filtered_lines)
        
        # Replace cell separators with proper function/class structure
        cleaned_content = re.sub(r'# %%[^\n]*\n', '\n\n', cleaned_content)
        
        # Add proper module header
        module_name = re.sub(r'[^\w]', '_', info['title']).lower()
        # Clean up multiple underscores and remove leading/trailing ones
        module_name = re.sub(r'_+', '_', module_name).strip('_')
        if not module_name:
            # Fallback to filename-based name
            module_name = re.sub(r'[^\w]', '_', Path(filepath).stem).lower()
            module_name = re.sub(r'_+', '_', module_name).strip('_')
        
        header = f'''"""
{info['title']}

Migrated from legacy generator: {info['filename']}
Subject Area: {subject_area}

This module contains educational content generators for MoodPy v3.0.0.
"""

import moodpy
from moodpy import Generator, Cloze
import numpy as np
import numpy.random as rnd

# Disable Sage HTML warnings if present
try:
    import sage.misc.html
    sage.misc.html._old_and_deprecated_behavior = False
except ImportError:
    pass

'''
        
        # Combine header with cleaned content
        final_content = header + cleaned_content
        
        # Create output path
        output_dir = self.subjects_dir / subject_area
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"{module_name}.py"
        
        # Write converted module
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
            
        # Create __init__.py if it doesn't exist
        init_file = output_dir / "__init__.py"
        if not init_file.exists():
            with open(init_file, 'w') as f:
                f.write(f'"""\\n{subject_area.title()} generators for MoodPy v3.0.0\\n"""\\n\\n')
                
        return {
            'input_file': filepath,
            'output_file': output_file,
            'module_name': module_name,
            'info': info
        }
        
    def migrate_high_priority_generators(self):
        """Migrate the highest priority generators first."""
        
        high_priority = [
            ("generators/MOODPY MAN 101 PRECIO DE EQUILIBRIO.py", "economics"),
            ("generators/Mate Financiera 104 Plazo de Inversión-checkpoint.py", "finance"),
            ("generators/P301_fp_lin_nr.py", "mathematics"),
            ("generators/PEP201_corr_discreta.py", "statistics"),
        ]
        
        results = []
        for filepath, subject in high_priority:
            if os.path.exists(filepath):
                try:
                    result = self.convert_to_module(filepath, subject)
                    results.append(result)
                    print(f"Migrated: {filepath} -> {result['output_file']}")
                except Exception as e:
                    print(f"Error migrating {filepath}: {e}")
                    
        return results


def main():
    migrator = GeneratorMigrator()
    
    if len(sys.argv) == 3:
        # Single file migration
        generator_file = sys.argv[1]
        subject_area = sys.argv[2]
        
        if not os.path.exists(generator_file):
            print(f"Error: Generator file not found: {generator_file}")
            return 1
            
        try:
            result = migrator.convert_to_module(generator_file, subject_area)
            print(f"Successfully migrated {generator_file}")
            print(f"Output: {result['output_file']}")
            print(f"Module: {result['module_name']}")
            return 0
        except Exception as e:
            print(f"Error: {e}")
            return 1
            
    elif len(sys.argv) == 1:
        # Batch migration of high priority generators
        print("Migrating high-priority generators...")
        results = migrator.migrate_high_priority_generators()
        print(f"\\nMigrated {len(results)} generators successfully.")
        return 0
        
    else:
        print(__doc__)
        return 1


if __name__ == "__main__":
    sys.exit(main())