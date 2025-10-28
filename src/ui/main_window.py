"""Main window implementation for the assembler lexer analyzer.

This module contains the MainWindow class that extends IngotApp to provide
a graphical user interface for the assembler lexer analyzer.
"""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtWidgets import QFileDialog, QHeaderView, QSplitter, QTableWidget, QTextEdit, QVBoxLayout
from PyQt6.QtCore import Qt
from ingot.app import IngotApp
from ingot.views.base import BaseView


class AsmLexerView(BaseView):
    """Custom view for the assembler lexer analyzer application."""
    
    def __init__(self):
        super().__init__()
        
        # Create horizontal splitter for main layout
        central_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Panel izquierdo para el código fuente
        self.source_code_view = QTextEdit()
        self.source_code_view.setPlaceholderText("Abre un archivo .asm para empezar...")

        # Panel derecho para los resultados (una tabla es mejor que texto plano)
        self.results_view = QTableWidget()
        self.results_view.setColumnCount(3)
        self.results_view.setHorizontalHeaderLabels(["#", "Elemento", "Tipo"])
        # Make the "Elemento" column stretch to fill available space
        header = self.results_view.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        # Add panels to the splitter
        central_splitter.addWidget(self.source_code_view)
        central_splitter.addWidget(self.results_view)

        # Add the splitter to the main layout
        self.layout().addWidget(central_splitter)


class MainWindow(IngotApp):
    """Main window for the assembler lexer analyzer application."""

    def __init__(self):
        """Initialize the main window with UI elements and menu."""
        # Define the view configuration
        view_config = {
            "title": "Analizador Léxico - Ensamblador",
            "view_factory": AsmLexerView  # Provide our custom view factory
        }
        
        # Initialize the parent IngotApp with view_config
        super().__init__(view_config=view_config)
        
        # Set the window title
        self.setWindowTitle("Analizador Léxico - Ensamblador")
        
        # Access the UI components from the view in the current tab
        # For custom views like ours, the tab widget IS the view itself
        current_tab = self.workspace.currentWidget()  # This might be our AsmLexerView directly
        if current_tab:
            # Check if current_tab has the UI components directly (it should be our AsmLexerView)
            if hasattr(current_tab, 'source_code_view'):
                self.source_code_view = current_tab.source_code_view
                self.results_view = current_tab.results_view
            else:
                # If the current tab doesn't have the components, try accessing via .widget() method
                # in case it is a container (like QScrollArea)
                try:
                    view_widget = current_tab.widget()
                    if hasattr(view_widget, 'source_code_view'):
                        self.source_code_view = view_widget.source_code_view
                        self.results_view = view_widget.results_view
                    else:
                        # Fallback: create placeholder attributes
                        self.source_code_view = None
                        self.results_view = None
                except AttributeError:
                    # If current_tab doesn't have a .widget() method, it's our view directly
                    self.source_code_view = None
                    self.results_view = None
        else:
            # Fallback: create placeholder attributes
            self.source_code_view = None
            self.results_view = None

    def _connect_zoom_signals(self):
        """
        Override to avoid zoom signal connection for text-based view.
        Our text-based AsmLexerView doesn't have zoom functionality.
        """
        # Don't connect zoom signals for this type of application
        pass

        # Define menu structure and actions
        self._setup_menu()
        
        # Create central widget layout
        self._setup_central_widget()

        # Initialize UI components
        self.source_code_view: QTextEdit | None = None
        self.results_view: QTableWidget | None = None

    def _setup_menu(self) -> None:
        """Setup the menu bar with required actions."""
        menu_config = {
            "Archivo": [
                {"id": "file.open", "name": "Abrir Archivo...", "shortcut": "Ctrl+O", "function": self.open_file_dialog},
                {"id": "file.exit", "name": "Salir", "shortcut": "Escape", "function": self.close}
            ],
            "Análisis": [
                {"id": "analysis.run", "name": "Analizar Código", "shortcut": "F5", "function": self.analyze_code}
            ]
        }
        self.set_menu(menu_config)

    def _setup_central_widget(self) -> None:
        """Setup is now handled in the AsmLexerView class."""
        # The central widget is now handled by the AsmLexerView
        # This method is kept for API compatibility but is not needed
        pass

    def open_file_dialog(self) -> None:
        """Open a file dialog to select an .asm file and display its content."""
        # Define the starting directory as the examples folder in the project
        examples_path = Path(__file__).parent.parent.parent / "examples"
        if not examples_path.exists():
            examples_path = Path.cwd() / "examples"
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo .asm",
            str(examples_path),
            "Archivos de ensamblador (*.asm *.s *.nasm)"
        )
        
        if file_path:
            try:
                # Read the file content and display it
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Update the source code view - get the view from the current tab
                current_tab = self.workspace.currentWidget()
                if current_tab:
                    # Check if current_tab is our AsmLexerView directly
                    if hasattr(current_tab, 'source_code_view'):
                        current_tab.source_code_view.setPlainText(content)
                    else:
                        # If current_tab is a container widget, try to get its widget
                        try:
                            view_widget = current_tab.widget()
                            if view_widget and hasattr(view_widget, 'source_code_view') and view_widget.source_code_view:
                                view_widget.source_code_view.setPlainText(content)
                        except AttributeError:
                            # It's not a container that supports .widget()
                            pass
                
                # Update status bar with the loaded file name
                file_name = Path(file_path).name
                if hasattr(self, 'status_bar') and self.status_bar:
                    try:
                        # Use the proper method for the status bar
                        self.status_bar.showMessage(f"Archivo cargado: {file_name}")
                    except AttributeError:
                        # qt-ingot StatusBar doesn't have showMessage, so just print to console
                        print(f"Archivo cargado: {file_name}")
                    
            except Exception as e:
                if hasattr(self, 'status_bar') and self.status_bar:
                    try:
                        # Use the proper method for the status bar
                        self.status_bar.showMessage(f"Error al leer el archivo: {str(e)}")
                    except AttributeError:
                        # qt-ingot StatusBar doesn't have showMessage, so just print to console
                        print(f"Error al leer el archivo: {str(e)}")

    def analyze_code(self) -> None:
        """Placeholder method for analyzing the loaded code."""
        # This will be implemented in Phase 3
        print("Función de análisis no implementada aún")
        
        # Clear the results view - get the current view to access the table
        current_tab = self.workspace.currentWidget()
        if current_tab:
            # Check if current_tab is our AsmLexerView directly
            if hasattr(current_tab, 'results_view'):
                current_tab.results_view.setRowCount(0)  # Clear existing rows
            else:
                # If current_tab is a container widget, try to get its widget
                try:
                    view_widget = current_tab.widget()
                    if view_widget and hasattr(view_widget, 'results_view') and view_widget.results_view:
                        view_widget.results_view.setRowCount(0)  # Clear existing rows
                except AttributeError:
                    # It's not a container that supports .widget()
                    pass
        
        if hasattr(self, 'status_bar') and self.status_bar:
            try:
                self.status_bar.showMessage("Análisis no implementado aún")
            except AttributeError:
                # qt-ingot StatusBar doesn't have showMessage, so just print to console
                print("Análisis no implementado aún")