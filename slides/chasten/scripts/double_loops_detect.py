"""
A script to detect doubly-nested for loops in a Python project.

This script walks through a directory, parses each Python file into an
Abstract Syntax Tree (AST), and checks for for-loops nested inside other
for-loops. The results are saved to a JSON file.
"""

import ast
import json
import os
import sys

class ForVisitor(ast.NodeVisitor):
    """
    An AST visitor that detects doubly-nested for loops.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.nested_for_loops = []
        self._for_depth = 0

    def visit_For(self, node):
        """
        Visit a for-loop node in the AST.
        """
        self._for_depth += 1
        if self._for_depth > 1:
            self.nested_for_loops.append({
                "file": self.filepath,
                "line": node.lineno,
                "col": node.col_offset
            })
        self.generic_visit(node)
        self._for_depth -= 1

def analyze_directory(directory):
    """
    Analyze all Python files in a directory for doubly-nested for loops.
    """
    all_nested_loops = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as source_file:
                    try:
                        tree = ast.parse(source_file.read(), filename=filepath)
                        visitor = ForVisitor(filepath)
                        visitor.visit(tree)
                        all_nested_loops.extend(visitor.nested_for_loops)
                    except SyntaxError as e:
                        print(f"Could not parse {filepath}: {e}")
    return all_nested_loops

def main():
    """
    Main function to run the analysis and save the results.
    """
    if len(sys.argv) != 2:
        print("Usage: python double_loops_detect.py <directory>")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_directory = os.path.join(script_dir, '..', sys.argv[1])
    if not os.path.isdir(target_directory):
        print(f"Error: '{target_directory}' is not a valid directory.")
        sys.exit(1)

    results = analyze_directory(target_directory)

    output_filename = "nested_loops.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Analysis complete. Found {len(results)} doubly-nested for-loops.")
    print(f"Results saved to {output_filename}")

if __name__ == "__main__":
    main()
