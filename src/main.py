"""Main entry point for the 8086 assembly lexer CLI tool."""

from __future__ import annotations

import sys
from pathlib import Path

# Add the src directory to the path so we can import from core
sys.path.insert(0, str(Path(__file__).parent.parent))

import typer
from rich.console import Console
from rich.table import Table

from src.core.lexer import Lexer

app = typer.Typer(name="asm-lexer", help="CLI tool for 8086 assembly lexical analysis.")
console = Console()


@app.command()
def analyze(
    file_path: str = typer.Argument(..., help="Path to the assembly file to analyze."),
) -> None:
    """Analyze an assembly file and display the lexical tokens."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except FileNotFoundError:
        console.print(f"[bold red]Error: File '{file_path}' not found.[/bold red]")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Error reading file: {e}[/bold red]")
        raise typer.Exit(code=1)
    
    lexer = Lexer(source_code)
    tokens = lexer.analyze()
    
    # Create a rich table to display the tokens
    table = Table(title=f"Lexical Analysis Results for {file_path}")
    table.add_column("#", justify="right", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    table.add_column("Type", style="green")
    table.add_column("Line", justify="right", style="yellow")
    
    for i, token in enumerate(tokens, start=1):
        table.add_row(str(i), token.value, token.type, str(token.line))
    
    console.print(table)
    console.print(f"\n[bold]Total tokens found: {len(tokens)}[/bold]")


@app.command()
def demo() -> None:
    """Run a demonstration of the lexer with sample code."""
    sample_code = """
    .DATA SEGMENT
        msg DB 'Hello, World!', 10, 13, '$'
        num DW 123
    .DATA ENDS
    
    .CODE SEGMENT
    START:
        MOV AX, @DATA
        MOV DS, AX
        
        LEA DX, msg
        MOV AH, 09h
        INT 21h
        
        MOV AH, 4Ch
        INT 21h
    .CODE ENDS
    END START
    """
    
    lexer = Lexer(sample_code)
    tokens = lexer.analyze()
    
    # Create a rich table to display the tokens
    table = Table(title="Demo: Lexical Analysis Results")
    table.add_column("#", justify="right", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    table.add_column("Type", style="green")
    table.add_column("Line", justify="right", style="yellow")
    
    for i, token in enumerate(tokens, start=1):
        table.add_row(str(i), token.value, token.type, str(token.line))
    
    console.print(table)
    console.print(f"\n[bold]Total tokens found: {len(tokens)}[/bold]")


if __name__ == "__main__":
    app()