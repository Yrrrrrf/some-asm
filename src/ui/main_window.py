"""Main window for the 8086 assembly lexer UI."""

from __future__ import annotations

from ingot.app import IngotApp


class MainWindow(IngotApp):
    """Main window for the assembly lexer application."""
    
    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()
        
        # Set window properties
        self.config.title = "8086 Assembly Lexer"
        self.config.icon = None  # Set an appropriate icon path later
        
        # Define menu configuration
        MENU_CONFIG = {
            "Archivo": [
                {"name": "Abrir Archivo...", "shortcut": "Ctrl+O", "function": self.open_file_dialog},
                {"name": "Exit", "shortcut": "Esc", "function": self.close}
            ],
            "Análisis": [
                {"name": "Analizar Código", "shortcut": "F5", "function": self.analyze_code}
            ]
        }
        self.set_menu(MENU_CONFIG)
    
    def open_file_dialog(self) -> None:
        """Placeholder for opening a file dialog."""
        print("Función no implementada: Abrir archivo")
    
    def analyze_code(self) -> None:
        """Placeholder for analyzing the code."""
        print("Función no implementada: Analizar código")