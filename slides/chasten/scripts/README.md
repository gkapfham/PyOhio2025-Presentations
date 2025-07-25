# Chasten Configuration for Doubly-Nested For Loops

## Overview

This directory contains a chasten configuration file and supporting materials
for detecting doubly-nested for loops in Python code. This example does not
yet work correctly on NixOS due to out-of-date dependencies in `chasten`.

## Files

- `chasten-config.yml` - Chasten configuration file for detecting doubly-nested for loops
- `shell.nix` - Nix shell environment for running chasten on NixOS
- `shell-simple.nix` - Simplified Nix shell environment 
- `chasten-demo.py` - Demonstration script showing how the analysis works
- `test_project/` - Sample Python files for testing
- `chasten-results.json` - Output from demonstration script

## Chasten Configuration

The `chasten-config.yml` file contains the following configuration:

```yaml
chasten:
  checks:
    - id: "CHA001"
      name: "doubly-nested-for-loops"
      description: "Detect doubly-nested for loops in Python code"
      pattern: './/For[ancestor::For]'
      min: 0
      max: 10
```

This configuration:
- Uses XPath pattern `.//For[ancestor::For]` to find For nodes with For ancestors
- Allows 0-10 matches (adjust max as needed)
- Provides a clear description and ID for the check

## Running Chasten

### On Standard Systems

```bash
# Install and run chasten
uvx chasten analyze --config chasten-config.yml test_project/
```

### On NixOS

Due to compilation issues with chasten's dependencies on NixOS, use the Nix shell environment:

```bash
# Enter the Nix shell environment
nix-shell shell.nix

# Then run chasten
uvx chasten analyze --config chasten-config.yml test_project/
```

### Alternative: Demonstration Script

If chasten installation fails, you can use the demonstration script that simulates the same functionality:

```bash
# Run the demo script
python3 chasten-demo.py
```

## Expected Output

The analysis should detect doubly-nested for loops in:
- `test_project/bad.py` at line 4, column 8
- `test_project/subdir/also_bad.py` at line 8, column 12

The file `test_project/good.py` contains only single for loops and should not trigger the pattern.

## Test Files

### bad.py (Contains doubly-nested for loop)
```python
def process_data(data):
    for row in data:
        for item in row:  # <- This triggers the pattern
            print(item)
```

### good.py (Single for loop only)
```python
def process_simple(data):
    for item in data:  # <- This does not trigger the pattern
        print(item)
```

## Troubleshooting

If you encounter compilation errors with chasten on NixOS:

1. Try using the provided `shell.nix` environment
2. Use the `chasten-demo.py` script as an alternative
3. Consider using chasten on a different system if available

The demonstration script provides the same core functionality and shows exactly
what chasten would detect with this configuration. Please note that the
`chasten-demo.py` file is _not_ a demonstration of `chasten`, per se, but
rather a demonstration of a `chasten`-like analysis for a specific feature.
