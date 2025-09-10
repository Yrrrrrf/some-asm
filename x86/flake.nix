# x86/flake.nix
{
  description = "Entorno de desarrollo para ensamblador x86";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: let
    # Define the system for which we are building
    system = "x86_64-linux";
    # Get the packages for that system
    pkgs = nixpkgs.legacyPackages.${system};

    # Define the custom script to compile and run .asm files
    run-asm = pkgs.writeShellScriptBin "run-asm" ''
      #!/usr/bin/env bash

      # --- 1. Validation ---
      # Check if an argument was provided
      if [ -z "$1" ]; then
          echo "Usage: run-asm <filename.asm>"
          exit 1
      fi

      SOURCE_FILE="$1"

      # Check if the provided file exists
      if [ ! -f "$SOURCE_FILE" ]; then
          echo "Error: File '$SOURCE_FILE' not found."
          exit 1
      fi

      # --- 2. Compilation & Execution ---
      # Get the base name of the file (e.g., "hello" from "scripts/hello.asm")
      BASENAME=$(basename "$SOURCE_FILE" .asm)
      OUTPUT_FILE="$BASENAME.com"

      echo "--- Compiling: $SOURCE_FILE -> $OUTPUT_FILE ---"
      # Compile the .asm file into a .com binary using nasm
      nasm -f bin "$SOURCE_FILE" -o "$OUTPUT_FILE"

      # Check if compilation was successful
      if [ $? -ne 0 ]; then
          echo "Error: Compilation failed."
          exit 1
      fi

      echo "--- Executing: $OUTPUT_FILE with emu2 ---"
      # Execute the compiled program with the emu2 emulator
      emu2 "$OUTPUT_FILE"
      echo "--- Done ---"
    '';

  in {
    # The key is to name the shell "default"
    devShells.${system}.default = pkgs.mkShell {
      # Packages that will be available in our environment
      packages = [
        pkgs.nasm
        pkgs.emu2
        run-asm  # Add our new script to the environment's PATH
      ];

      # Welcome message
      shellHook = ''
        echo "¡x8086 ENV Ready!"
        echo "-------------------------------------"
        echo "Available tools: nasm, emu2"
        echo "Custom command: run-asm <file.asm>"
      '';
    };
  };
}
