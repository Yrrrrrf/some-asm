#!/usr/bin/env python3
"""
dis-asm.py - Capstone Disassembler Example

This script demonstrates the Capstone disassembly library with real x86 assembly examples.
It showcases how to disassemble binary code and analyze assembly instructions.
"""

import argparse
import os
from capstone import *  # pylint: disable=wildcard-import,unused-wildcard-import


def read_asm_file(asm_file_path: str) -> bytes:
    """
    Read an assembly file and return its content as bytes.
    This is a simplified version that will look for a corresponding binary file 
    or use a basic heuristic to extract binary data.
    """
    # Look for a compiled binary file first (.com, .bin, etc.)
    base_path = os.path.splitext(asm_file_path)[0]
    possible_binary_paths = [
        f"{base_path}.com", 
        f"{base_path}.bin",
        asm_file_path.replace(".asm", ".com"),
        asm_file_path.replace(".asm", ".bin")
    ]
    
    for bin_path in possible_binary_paths:
        if os.path.exists(bin_path):
            with open(bin_path, 'rb') as f:
                return f.read()
    
    # If no binary file exists, return empty bytes
    # In a real implementation, we'd compile the file, but for this demo,
    # we'll show how you could compile using an external command
    print(f"Binary file not found for {asm_file_path}")
    print(f"Expected one of: {', '.join(possible_binary_paths)}")
    print(f"Hint: You may need to compile the assembly file first using NASM")
    print(f"Example: nasm -f bin {asm_file_path} -o {base_path}.com")
    return b""


def disassemble_code(code: bytes, arch: int, mode: int, start_address: int = 0x0) -> None:
    """
    Disassemble binary code using Capstone.

    Args:
        code: The binary code to disassemble
        arch: Architecture (e.g., CS_ARCH_X86)
        mode: Mode (e.g., CS_MODE_16)
        start_address: Starting address for disassembly
    """
    if not code:
        print("No binary code to disassemble.")
        return
    
    try:
        # Initialize the disassembler
        md = Cs(arch, mode)

        print(f"Disassembling {len(code)} bytes:")
        print("-" * 60)

        # Disassemble the code and print each instruction
        for insn in md.disasm(code, start_address):
            # Format the bytes as hex
            bytes_str = " ".join(f"{b:02x}" for b in insn.bytes)
            # Print the instruction details
            print(f"0x{insn.address:08x}: {bytes_str:<20} {insn.mnemonic:<10} {insn.op_str}")

    except CsError as e:
        print(f"Capstone error: {e}")


def main() -> None:
    """Main function demonstrating Capstone disassembler capabilities."""
    parser = argparse.ArgumentParser(
        description="Capstone Disassembler - Analyze x86 Assembly Files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s path/to/file.asm             # Disassemble a specific assembly file
  %(prog)s --arch x86-16 path/to/file.asm  # Disassemble with 16-bit mode (default)
  %(prog)s --arch x86-32 path/to/file.asm  # Disassemble with 32-bit mode
  %(prog)s --arch x86-64 path/to/file.asm  # Disassemble with 64-bit mode
        """
    )
    parser.add_argument(
        "--arch",
        choices=["x86-16", "x86-32", "x86-64"],
        default="x86-16",
        help="Architecture to disassemble (default: x86-16)"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to the assembly file to disassemble (.asm)"
    )
    
    args = parser.parse_args()
    
    # Determine architecture and mode based on argument
    arch_modes = {
        "x86-16": (CS_ARCH_X86, CS_MODE_16),
        "x86-32": (CS_ARCH_X86, CS_MODE_32),
        "x86-64": (CS_ARCH_X86, CS_MODE_64)
    }
    
    arch, mode = arch_modes[args.arch]
    
    print("Capstone Disassembler - Analyzing Assembly Files")
    print("=" * 60)
    print(f"Architecture: {args.arch.upper()}")
    
    if args.file:
        # Process the specified file
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' does not exist.")
            return
        
        print(f"File: {args.file}")
        print()
        
        # Read the assembly file and disassemble
        binary_code = read_asm_file(args.file)
        disassemble_code(binary_code, arch, mode, 0x100)
        
        if not binary_code:
            print("\nTo properly disassemble an assembly file, you need to:")
            print("1. Compile it first: nasm -f bin", args.file, f"-o {os.path.splitext(args.file)[0]}.com")
            print("2. Then run this script again")
    else:
        # Show a simple example if no file provided
        print("\nNo assembly file specified.")
        print("Usage: dis-asm.py [options] <asm_file.asm>")
        print("\nTo disassemble an assembly file, provide a path to the .asm file.")
        print("Note: You'll need to compile the .asm file to binary format first.")


if __name__ == "__main__":
    main()
