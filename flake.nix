{
  description = "Python development environment with venv";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python312;
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python
            python312Packages.pip
            python312Packages.virtualenv
          ];

          shellHook = ''
            if [ ! -d .venv ]; then
              echo "Creating virtual environment..."
              ${python}/bin/python -m venv .venv
            fi
            
            echo "Activating virtual environment..."
            source .venv/bin/activate
            
            echo "Python development environment ready!"
            echo "Python version: $(python --version)"
          '';
        };
      }
    );
}
