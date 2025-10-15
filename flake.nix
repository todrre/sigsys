{
  description = "Sigsys group project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        # Use Python 3.13 so the corresponding python313Packages are available
        python = pkgs.python313;

        # Project Python environment: add project dependencies here.
        # Use the python313 package set so `control` resolves to
        pythonEnv = python.withPackages (ps: with ps; [
          control
          matplotlib
          numpy
          ipywidgets
          jupyter
          ipykernel
          notebook
        ]);

        # Useful CLI tools for development (optional). Include/omit as you like.
        cliTools = with pkgs; [
          # curl 
        ];
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            pythonEnv # Python environment with project dependencies
          ] ++ cliTools;

          shellHook = ''
            echo "Dev shell: ${toString system}"
            echo "Python: $(python --version)"
            echo "Type 'exit' to leave the shell"
          '';
        };
      });
}
