"""Main entry point for the assembler lexer analyzer application.

This module initializes and runs the main application window.
"""

import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from rich.console import Console
from rich.text import Text

# Add the src directory to Python path to allow imports
sys.path.insert(0, str(Path(__file__).parent))

from ui.main_window import MainWindow


def main() -> None:
    """Main entry point of the application."""
    # Print project name in blue and version in green italic
    console = Console()
    output = Text()
    output.append("some-asm", style="blue")
    output.append(" ")
    output.append("v0.1.0", style="green italic")
    console.print(output)

    # Initialize Qt application
    app = QApplication(sys.argv)
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Execute the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()