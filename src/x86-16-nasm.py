#!/usr/bin/env python3
"""
x86-16-nasm.py - Run x86-16 assembly files with rich output

This script provides a user-friendly interface for running x86-16 assembly files
with enhanced visual feedback using Rich. It can automatically locate assembly
files in the examples directory.
"""

import argparse
import subprocess
import tempfile
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.text import Text
from rich.table import Table
from rich import print as rprint
import sys


def find_asm_file(user_input: str) -> str:
    """
    Find an assembly file based on user input.
    
    Args:
        user_input: The user-provided file path or name
        
    Returns:
        The full path to the assembly file
    """
    # If the user provided an absolute or relative path that exists, use it directly
    if os.path.exists(user_input):
        return user_input
    
    # If it's just a filename without path, search in examples directory
    base_name = os.path.basename(user_input)
    if not base_name.endswith('.asm'):
        base_name += '.asm' if not user_input.endswith('.asm') else ''
    
    # Search for the file in the examples directory
    for root, dirs, files in os.walk("examples"):
        for file in files:
            if file == base_name:
                return os.path.join(root, file)
    
    # If not found, return None
    return None


def compile_asm(asm_file: str, console: Console) -> tuple[bool, str]:
    """
    Compile an assembly file to binary using NASM.
    
    Args:
        asm_file: Path to the assembly file to compile
        console: Rich console for output
        
    Returns:
        tuple: (success: bool, output_file_path: str)
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".com") as temp_output:
        output_file = temp_output.name
    
    try:
        # Using Rich progress bar to show compilation
        with console.status("[bold green]Compiling assembly...", spinner="clock") as status:
            # Compile the assembly file to binary using NASM
            result = subprocess.run([
                "nasm", 
                "-f", "bin",  # Output format: binary
                asm_file, 
                "-o", output_file
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                console.print(f"[green]✓[/green] Successfully compiled {asm_file}")
                return True, output_file
            else:
                console.print(f"[red]✗[/red] Compilation failed: {result.stderr}")
                return False, ""
    
    except FileNotFoundError:
        console.print("[red]✗[/red] NASM not found. Please install NASM or run in nix environment.")
        return False, ""


def execute_binary(binary_file: str, console: Console, args: list = []) -> bool:
    """
    Execute the compiled binary using emu2.
    
    Args:
        binary_file: Path to the compiled binary
        console: Rich console for output
        args: Additional arguments to pass to the program
        
    Returns:
        bool: True if execution was successful
    """
    try:
        console.print("[bold blue]Executing program... (Press Ctrl+C to exit)[/bold blue]")
        # Execute the compiled program with the emu2 emulator interactively
        # We don't capture output here so user can interact with the program
        result = subprocess.run([
            "emu2", 
            binary_file
        ] + args)
        
        # For interactive programs, we consider any execution as success
        # since the program might exit with a non-zero code after user interaction
        console.print(f"[green]✓[/green] Program execution completed")
        return True
    
    except FileNotFoundError:
        console.print("[red]✗[/red] emu2 not found. Please install emu2 or run in nix environment.")
        return False
    except KeyboardInterrupt:
        console.print(f"\n[yellow]⚠[/yellow] Program interrupted by user")
        return True  # Consider interruption as expected behavior for interactive programs


def cleanup_file(file_path: str, console: Console):
    """
    Remove the specified file.
    
    Args:
        file_path: Path to the file to remove
        console: Rich console for output
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            console.print(f"[blue]✓[/blue] Cleaned up {file_path}")
    except OSError as e:
        console.print(f"[red]✗[/red] Failed to clean up {file_path}: {e}")


def display_asm_info(asm_file: str, console: Console):
    """
    Display information about the assembly file.
    
    Args:
        asm_file: Path to the assembly file
        console: Rich console for output
    """
    path = Path(asm_file)
    
    table = Table(title="Assembly File Information")
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    
    table.add_row("File Name", path.name)
    table.add_row("Full Path", str(path.absolute()))
    table.add_row("Size", f"{path.stat().st_size} bytes")
    table.add_row("Last Modified", str(path.stat().st_mtime))
    
    console.print(table)


def main():
    parser = argparse.ArgumentParser(
        description="Run x86-16 assembly files with rich output",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s hello.asm           # Run hello.asm from examples directory
  %(prog)s path/to/file.asm    # Run assembly file at specific path
  %(prog)s skeleton            # Run skeleton.asm (extension optional)
        """
    )
    
    parser.add_argument(
        "file",
        help="Path to the assembly file to run (.asm extension optional)"
    )
    
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Don't delete the compiled binary after execution"
    )
    
    args = parser.parse_args()
    
    # Initialize Rich console
    console = Console()
    
    # Find the assembly file
    asm_file = find_asm_file(args.file)
    if not asm_file:
        console.print(f"[red]✗[/red] Assembly file '{args.file}' not found in examples directory or as absolute path.")
        # Show available assembly files
        asm_files = []
        for root, dirs, files in os.walk("examples"):
            for file in files:
                if file.endswith('.asm'):
                    asm_files.append(os.path.relpath(os.path.join(root, file), "."))
        
        if asm_files:
            console.print("\n[bold]Available assembly files:[/bold]")
            for asm_file_path in asm_files[:10]:  # Show first 10 files
                console.print(f"  - {asm_file_path}")
            if len(asm_files) > 10:
                console.print(f"  ... and {len(asm_files) - 10} more")
        else:
            console.print("[yellow]No assembly files found in examples directory.[/yellow]")
        return 1
    
    console.print(Panel(f"[bold blue]x86-16 Assembly Runner[/bold blue]\n[green]{asm_file}[/green]", expand=False))
    
    # Display file information
    display_asm_info(asm_file, console)
    
    # Compile the assembly file
    success, binary_file = compile_asm(asm_file, console)
    if not success:
        return 1
    
    # Execute the binary
    exec_success = execute_binary(binary_file, console)
    
    # Clean up unless --no-cleanup was specified
    if not args.no_cleanup:
        cleanup_file(binary_file, console)
    
    # Final status
    if exec_success:
        console.print(Panel("[bold green]✓ SUCCESS[/bold green] Assembly file executed successfully!", expand=False))
        return 0
    else:
        console.print(Panel("[bold red]✗ FAILED[/bold red] Assembly file execution failed!", expand=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
