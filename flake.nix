{
  description = "A python devshell";

  inputs.nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";

  outputs = { self, nixpkgs}:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.x86_64-linux.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          hello
        ];
        packages = [
          (pkgs.python3.withPackages(p: with p; [
            pillow
            pygame-ce
            numpy
            pandas
            pytest
          ]))
        ];
        shellHook = ''
          echo "Welcome back, your game awaits..."
        '';
      };
    };
}
