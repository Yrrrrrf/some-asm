# x86/flake.nix
{
  description = "Entorno de desarrollo para ensamblador x86";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
  in {
    devShells.${system}.default = pkgs.mkShell {
      packages = [
        pkgs.nasm
        pkgs.emu2
        (pkgs.writeShellScriptBin "run-asm" (builtins.readFile ./run-asm.sh))
      ];
      shellHook = ''
        echo "¡x8086 ENV Ready!"
        echo "-------------------------------------"
        echo "Available tools: nasm, emu2"
        echo "Custom command: run-asm <file.asm>"
      '';
    };
  };
}

