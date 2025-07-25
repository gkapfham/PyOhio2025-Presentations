#!/usr/bin/env python3
"""
Demonstration script showing how chasten configuration works.
This simulates what chasten would do with the config file.
"""

import ast
import json
import sys
from pathlib import Path

def find_doubly_nested_for_loops(file_path):
    """Find doubly-nested for loops in a Python file using AST."""
    results = []
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=file_path)
        
        class ForLoopVisitor(ast.NodeVisitor):
            def __init__(self):
                self.for_depth = 0
                self.matches = []
            
            def visit_For(self, node):
                self.for_depth += 1
                if self.for_depth > 1:
                    self.matches.append({
                        "file": str(file_path),
                        "line": node.lineno,
                        "col": node.col_offset,
                        "pattern": "doubly-nested-for-loops"
                    })
                self.generic_visit(node)
                self.for_depth -= 1
        
        visitor = ForLoopVisitor()
        visitor.visit(tree)
        results.extend(visitor.matches)
        
    except (SyntaxError, FileNotFoundError) as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
    
    return results

def main():
    """Main function simulating chasten analyze command."""
    target_dir = Path("test_project")
    
    if not target_dir.exists():
        print(f"Error: Directory {target_dir} not found")
        return 1
    
    print("📋 Chasten Configuration Simulation")
    print("=" * 50)
    print(f"🔍 Scanning directory: {target_dir}")
    print("🎯 Pattern: Doubly-nested for loops")
    print()
    
    all_matches = []
    python_files = list(target_dir.rglob("*.py"))
    
    if not python_files:
        print("❌ No Python files found in directory")
        return 1
    
    print(f"📁 Found {len(python_files)} Python files:")
    for py_file in python_files:
        print(f"  • {py_file}")
    print()
    
    for py_file in python_files:
        matches = find_doubly_nested_for_loops(py_file)
        all_matches.extend(matches)
    
    print("🎯 Analysis Results:")
    print("=" * 30)
    
    if all_matches:
        print(f"✅ Found {len(all_matches)} doubly-nested for loop(s):")
        print()
        for i, match in enumerate(all_matches, 1):
            print(f"  {i}. File: {match['file']}")
            print(f"     Line: {match['line']}, Column: {match['col']}")
            print()
    else:
        print("❌ No doubly-nested for loops found")
    
    # Save results to JSON (like chasten would)
    output_file = "chasten-results.json"
    with open(output_file, 'w') as f:
        json.dump(all_matches, f, indent=2)
    
    print(f"💾 Results saved to: {output_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())