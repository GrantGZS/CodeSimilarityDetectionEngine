"""
Test file generator for code similarity detection.

This script generates ~50 test Python files with controlled similarity
by applying various mutation strategies to base templates.
"""

import os
import json
import random
import ast
import astor  # For converting AST back to code
from typing import List, Dict, Set, Tuple
from pathlib import Path


# Base templates - simple Python code snippets
TEMPLATES = [
    # Template 1: Simple function
    """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

def find_max(numbers):
    if not numbers:
        return None
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val
""",

    # Template 2: Class with methods
    """
class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, value):
        self.result += value
        return self.result
    
    def multiply(self, factor):
        self.result *= factor
        return self.result
    
    def reset(self):
        self.result = 0
""",

    # Template 3: List operations
    """
def process_list(items):
    result = []
    for item in items:
        if isinstance(item, int) and item > 0:
            result.append(item * 2)
        elif isinstance(item, str):
            result.append(item.upper())
    return result

def filter_even(numbers):
    return [num for num in numbers if num % 2 == 0]
""",

    # Template 4: Dictionary operations
    """
def count_words(text):
    words = text.split()
    word_count = {}
    for word in words:
        word = word.lower().strip('.,!?')
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

def get_most_common(word_count):
    if not word_count:
        return None
    return max(word_count.items(), key=lambda x: x[1])
""",

    # Template 5: Recursive function
    """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
"""
]


class CodeMutator:
    """Handles various code mutation strategies."""
    
    def __init__(self):
        self.variable_names = [
            'a', 'b', 'c', 'x', 'y', 'z', 'i', 'j', 'k', 'n', 'm',
            'temp', 'val', 'item', 'data', 'result', 'count', 'index'
        ]
    
    def rename_variables(self, code: str) -> str:
        """Randomly rename some variables in the code."""
        try:
            tree = ast.parse(code)
            renames = {}
            
            # Find all variable names
            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    if node.id not in ['self', '__init__', '__name__'] and random.random() < 0.3:
                        if node.id not in renames:
                            renames[node.id] = random.choice(self.variable_names)
            
            # Apply renames
            for old_name, new_name in renames.items():
                code = code.replace(f' {old_name} ', f' {new_name} ')
                code = code.replace(f'({old_name}', f'({new_name}')
                code = code.replace(f'{old_name})', f'{new_name})')
                code = code.replace(f'{old_name}.', f'{new_name}.')
                code = code.replace(f'{old_name}:', f'{new_name}:')
            
            return code
        except Exception as e:
            print(f"Warning: Variable renaming failed: {e}")
            return code  # Return original if parsing fails
    
    def change_indentation(self, code: str) -> str:
        """Randomly change indentation levels."""
        lines = code.split('\n')
        new_lines = []
        
        indent_change = random.choice([-1, 0, 1])
        
        for line in lines:
            stripped = line.lstrip()
            if stripped:  # Non-empty line
                current_indent = len(line) - len(stripped)
                new_indent = max(0, current_indent + indent_change * random.randint(0, 2))
                new_lines.append(' ' * new_indent + stripped)
            else:
                new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def add_dead_code(self, code: str) -> str:
        """Add dead code that doesn't affect logic."""
        lines = code.split('\n')
        dead_code_options = [
            '    pass',
            '    # This is a comment',
            '    unused_var = 42',
            '    if False: pass',
            '    try: pass except: pass'
        ]
        
        # Insert dead code at random positions
        if len(lines) > 0:
            insert_positions = random.sample(range(len(lines)), min(2, len(lines)))
            
            for pos in sorted(insert_positions, reverse=True):
                if random.random() < 0.5:
                    dead_line = random.choice(dead_code_options)
                    lines.insert(pos, dead_line)
        
        return '\n'.join(lines)
    
    def reorder_functions(self, code: str) -> str:
        """Reorder function/class definitions."""
        try:
            tree = ast.parse(code)
            functions = []
            other_code = []
            
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    functions.append(node)
                else:
                    other_code.append(node)
            
            # Shuffle functions
            random.shuffle(functions)
            
            # Reconstruct tree
            tree.body = other_code + functions
            
            return astor.to_source(tree)
        except Exception as e:
            print(f"Warning: Function reordering failed: {e}")
            return code  # Return original if parsing fails
    
    def apply_mutations(self, code: str) -> str:
        """Apply a random subset of mutations."""
        mutations = [
            self.rename_variables,
            self.change_indentation,
            self.add_dead_code,
            self.reorder_functions
        ]
        
        # Apply 1-3 random mutations
        selected = random.sample(mutations, random.randint(1, 3))
        
        for mutation in selected:
            code = mutation(code)
        
        return code


def generate_test_files(output_dir: str = "submissions", num_files: int = 50):
    """
    Generate test files with controlled similarity.
    
    Args:
        output_dir: Directory to save generated files
        num_files: Total number of files to generate
    """
    print("Starting test file generation...")
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    print(f"Created directory: {output_dir}")
    
    # Calculate files per template
    templates_count = len(TEMPLATES)
    files_per_template = num_files // templates_count
    extra_files = num_files % templates_count
    
    print(f"Generating {num_files} files from {templates_count} templates")
    print(f"Files per template: {files_per_template} (+{extra_files} extra)")
    
    mutator = CodeMutator()
    ground_truth = {}
    file_counter = 1
    
    for template_idx, template in enumerate(TEMPLATES):
        # Determine how many files for this template
        count = files_per_template + (1 if template_idx < extra_files else 0)
        
        template_files = []
        print(f"Processing template {template_idx + 1}: generating {count} files")
        
        for i in range(count):
            # Apply mutations
            mutated_code = mutator.apply_mutations(template)
            
            # Generate filename
            filename = f"test_{file_counter:04d}.py"
            filepath = os.path.join(output_dir, filename)
            
            # Write file
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(mutated_code)
                print(f"  Created: {filename}")
            except Exception as e:
                print(f"  Error creating {filename}: {e}")
                continue
            
            template_files.append(filename)
            file_counter += 1
        
        # Record ground truth for this template
        if len(template_files) > 1:
            # All pairs from same template are similar
            for file1 in template_files:
                ground_truth[file1] = [f for f in template_files if f != file1]
    
    # Save ground truth
    try:
        with open('ground_truth.json', 'w', encoding='utf-8') as f:
            json.dump(ground_truth, f, indent=2)
        print("Ground truth saved to ground_truth.json")
    except Exception as e:
        print(f"Error saving ground truth: {e}")
    
    print(f"Generated {num_files} test files in {output_dir}/")
    print(f"Files from same template are considered similar")


def validate_generation():
    """Validate that files were generated correctly."""
    print("Validating generation...")
    
    if not os.path.exists('submissions'):
        print("❌ submissions/ directory not found")
        return
    
    files = os.listdir('submissions')
    py_files = [f for f in files if f.endswith('.py')]
    
    print(f"✅ Found {len(py_files)} Python files in submissions/")
    
    if os.path.exists('ground_truth.json'):
        try:
            with open('ground_truth.json', 'r') as f:
                gt = json.load(f)
            print(f"✅ Ground truth loaded with {len(gt)} entries")
        except Exception as e:
            print(f"❌ Error loading ground truth: {e}")
    else:
        print("❌ ground_truth.json not found")


if __name__ == "__main__":
    print("Test Generator Starting...")
    
    # Check dependencies
    try:
        import astor
        print("✅ astor dependency available")
    except ImportError:
        print("❌ astor not installed. Run: pip install astor")
        exit(1)
    
    # Generate test files
    generate_test_files()
    
    # Validate
    validate_generation()
    
    print("\n🎉 Test file generation complete!")
    print("You can now run similarity detection on the submissions/ folder.")