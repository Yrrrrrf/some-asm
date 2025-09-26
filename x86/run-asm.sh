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

# --- 3. Cleanup ---
echo "--- Cleaning up: Removing $OUTPUT_FILE ---"
rm "$OUTPUT_FILE"
