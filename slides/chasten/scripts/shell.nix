{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    # Core development tools
    gcc
    stdenv.cc.cc.lib
    glibc
    glibc.dev
    
    # Build tools
    pkg-config
    cmake
    ninja
    gnumake
    
    # Python with development headers
    python3
    python3Packages.pip
    python3Packages.setuptools
    python3Packages.wheel
    python3Packages.scikit-build
    
    # Core libraries with development headers
    zlib
    zlib.dev
    libffi
    libffi.dev
    openssl
    openssl.dev
    libxml2
    libxml2.dev
    libxslt
    libxslt.dev
    
    # Try to include C library headers
    linuxHeaders
  ];

  shellHook = ''
    export NIX_CFLAGS_COMPILE="-I${pkgs.glibc.dev}/include $NIX_CFLAGS_COMPILE"
    export NIX_LDFLAGS="-L${pkgs.glibc}/lib $NIX_LDFLAGS"
    export C_INCLUDE_PATH="${pkgs.glibc.dev}/include:${pkgs.linuxHeaders}/include:$C_INCLUDE_PATH"
    export CPLUS_INCLUDE_PATH="${pkgs.glibc.dev}/include:${pkgs.linuxHeaders}/include:$CPLUS_INCLUDE_PATH"
    export LIBRARY_PATH="${pkgs.glibc}/lib:${pkgs.stdenv.cc.cc.lib}/lib:$LIBRARY_PATH"
    export LD_LIBRARY_PATH="${pkgs.glibc}/lib:${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH"
    
    # Set up Python environment
    export PYTHONPATH="${pkgs.python3}/lib/python3.12/site-packages:$PYTHONPATH"
    
    echo "Development environment loaded with GCC and compilation tools"
  '';
}
