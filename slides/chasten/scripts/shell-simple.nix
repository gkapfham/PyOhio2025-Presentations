{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python3Packages.pip
    python3Packages.setuptools
    python3Packages.wheel
    python3Packages.typer
    python3Packages.rich
    python3Packages.pyyaml
    python3Packages.lxml
    python3Packages.pathspec
    python3Packages.click
    gcc
    cmake
    ninja
  ];

  shellHook = ''
    # First try uvx with a simpler tool to verify it works
    echo "Development environment loaded"
    echo "Testing uvx with a simple tool..."
  '';
}