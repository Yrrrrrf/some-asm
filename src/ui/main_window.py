"""Main window implementation for the assembler lexer analyzer.

This module contains the MainWindow class that extends IngotApp to provide
a graphical user interface for the assembler lexer analyzer.
"""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtWidgets import QFileDialog, QHeaderView, QSplitter, QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout
from PyQt6.QtCore import Qt
from ingot.app import IngotApp
from ingot.views.base import BaseView
from ingot.theming.manager import ThemeManager

import sys
from pathlib import Path
# Add the src directory to the Python path so we can import from core
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from core.lexer import Lexer, Token

# Import sass for SCSS compilation
try:
    import sass
except ImportError:
    sass = None


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

        # Define menu structure and actions
        self._setup_menu()
        
        # Create central widget layout
        self._setup_central_widget()

        # Initialize UI components
        self.source_code_view: QTextEdit | None = None
        self.results_view: QTableWidget | None = None

        # Connect textChanged signal for real-time analysis
        self._connect_text_changed_signal()
        
        # Connect cursorPositionChanged signal for code-to-table synchronization
        self._connect_cursor_position_signal()
        
        # Connect itemSelectionChanged signal for table-to-code synchronization
        self._connect_table_selection_signal()
        
        # Apply Catppuccin theme
        self._apply_catppuccin_theme()
        
        # Initialize with empty analysis
        self.analyze_code()

    def _connect_zoom_signals(self):
        """
        Override to avoid zoom signal connection for text-based view.
        Our text-based AsmLexerView doesn't have zoom functionality.
        """
        # Don't connect zoom signals for this type of application
        pass

    def _connect_text_changed_signal(self) -> None:
        """Connect the textChanged signal for real-time analysis."""
        if self.source_code_view:
            self.source_code_view.textChanged.connect(self.analyze_code)

    def _connect_cursor_position_signal(self) -> None:
        """Connect the cursorPositionChanged signal for code-to-table synchronization."""
        if self.source_code_view:
            self.source_code_view.cursorPositionChanged.connect(self._sync_code_to_table)

    def _connect_table_selection_signal(self) -> None:
        """Connect the itemSelectionChanged signal for table-to-code synchronization."""
        current_tab = self.workspace.currentWidget()
        if not current_tab:
            return

        results_view = None
        if hasattr(current_tab, 'results_view'):
            results_view = current_tab.results_view
        else:
            try:
                view_widget = current_tab.widget()
                if view_widget and hasattr(view_widget, 'results_view'):
                    results_view = view_widget.results_view
            except AttributeError:
                pass

        if results_view:
            results_view.itemSelectionChanged.connect(self._sync_table_to_code)

    def _apply_catppuccin_theme(self) -> None:
        """Apply the Catppuccin theme using the existing ThemeManager."""
        if sass is None:
            # If sass is not available, try loading the existing theme through the manager
            try:
                # Try to apply a built-in theme as fallback
                if hasattr(self, 'theme_manager'):
                    self.theme_manager.apply_default_theme()
            except Exception:
                pass
            return
            
        try:
            # For now, we'll apply the theme by loading the SCSS content directly
            # The ThemeManager in qt-ingot works with predefined themes, so we'll set the stylesheet directly
            theme_path = Path(__file__).parent.parent.parent / "resources" / "themes" / "catppuccin-mocha.scss"
            if theme_path.exists():
                with open(theme_path, 'r') as f:
                    theme_content = f.read()
                
                # Use sass to compile SCSS to CSS
                compiled_css = sass.compile(string=theme_content)
                self.setStyleSheet(compiled_css)
            else:
                print(f"Theme file not found: {theme_path}")
        except Exception as e:
            print(f"Error applying theme: {str(e)}")
            # Fallback to default theme if custom theme fails
            if hasattr(self, 'theme_manager'):
                try:
                    self.theme_manager.apply_default_theme()
                except:
                    pass

    def _sync_table_to_code(self) -> None:
        """Synchronize from results table to code editor based on table selection."""
        if not self.source_code_view or not hasattr(self, 'current_tokens'):
            return

        current_tab = self.workspace.currentWidget()
        if not current_tab:
            return

        results_view = None
        if hasattr(current_tab, 'results_view'):
            results_view = current_tab.results_view
        else:
            try:
                view_widget = current_tab.widget()
                if view_widget and hasattr(view_widget, 'results_view'):
                    results_view = view_widget.results_view
            except AttributeError:
                pass

        if not results_view:
            return

        # Get currently selected row
        selected_items = results_view.selectedItems()
        if not selected_items:
            return

        # Get the row of the first selected item
        selected_row = selected_items[0].row()

        # Get the corresponding token
        if selected_row < len(self.current_tokens):
            token = self.current_tokens[selected_row]
            target_line = token.line

            # Move cursor to the target line in the source code editor
            cursor = self.source_code_view.textCursor()
            cursor.movePosition(cursor.MoveOperation.Start)  # Move to beginning
            cursor.movePosition(
                cursor.MoveOperation.Down,
                cursor.MoveMode.MoveAnchor,
                target_line - 1  # Lines are 1-indexed, positions are 0-indexed
            )
            self.source_code_view.setTextCursor(cursor)
            
            # Optionally scroll to make the line visible
            self.source_code_view.ensureCursorVisible()
            
            # Highlight the line
            self._highlight_current_line()

    def _highlight_current_line(self) -> None:
        """Highlight the current line in the source code editor."""
        if not self.source_code_view:
            return

        from PyQt6.QtGui import QTextCharFormat, QColor
        from PyQt6.QtCore import Qt

        # Create extra selection for line highlight
        extra_selections = []

        # Create a selection format for highlighting
        selection = QTextCharFormat()
        # Use Catppuccin surface color for highlighting
        selection.setBackground(QColor("#313244"))  # surface0 from Catppuccin
        selection.setForeground(QColor("#cdd6f4"))  # text from Catppuccin

        # Get the cursor
        cursor = self.source_code_view.textCursor()
        # Move to the start of the current block (line)
        cursor.movePosition(cursor.MoveOperation.StartOfBlock)
        # Move to the end of the current block (line) and select it
        cursor.movePosition(cursor.MoveOperation.EndOfBlock, cursor.MoveMode.KeepAnchor)

        # Create extra selection
        highlight_selection = self.source_code_view.ExtraSelection()
        highlight_selection.format = selection
        highlight_selection.cursor = cursor
        extra_selections.append(highlight_selection)

        # Apply the extra selections to highlight the line
        self.source_code_view.setExtraSelections(extra_selections)

    def _sync_code_to_table(self) -> None:
        """Synchronize from code editor to results table based on cursor position."""
        if not self.source_code_view or not hasattr(self, 'current_tokens'):
            return

        # Get current cursor position
        cursor = self.source_code_view.textCursor()
        current_line = cursor.blockNumber() + 1  # Block numbers are 0-indexed, so add 1

        # Find the first token in the current line
        current_tab = self.workspace.currentWidget()
        if not current_tab:
            return

        results_view = None
        if hasattr(current_tab, 'results_view'):
            results_view = current_tab.results_view
        else:
            try:
                view_widget = current_tab.widget()
                if view_widget and hasattr(view_widget, 'results_view'):
                    results_view = view_widget.results_view
            except AttributeError:
                pass

        if not results_view:
            return

        # Look for the first token in the current line in the table
        for row in range(results_view.rowCount()):
            if row < len(self.current_tokens):
                token = self.current_tokens[row]
                if token.line == current_line:
                    # Found the row corresponding to the current line
                    results_view.selectRow(row)
                    
                    # Get the item to scroll to
                    item = results_view.item(row, 0)  # Use first column item
                    if item:
                        results_view.scrollToItem(item)
                    break
        
        # Highlight the current line in the source code editor
        self._highlight_current_line()

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
                
                # Automatically analyze the loaded content to populate the table
                self.analyze_code()
                
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
        """Analyze the loaded code using the lexer and display results."""
        # Get the current tab to access the UI elements
        current_tab = self.workspace.currentWidget()
        if not current_tab:
            return

        # Get the source code from the editor
        source_code_view = None
        if hasattr(current_tab, 'source_code_view'):
            source_code_view = current_tab.source_code_view
        else:
            try:
                view_widget = current_tab.widget()
                if view_widget and hasattr(view_widget, 'source_code_view'):
                    source_code_view = view_widget.source_code_view
            except AttributeError:
                pass

        if not source_code_view:
            return

        source_code = source_code_view.toPlainText()
        
        # Create lexer instance and analyze the code
        lexer = Lexer(source_code)
        tokens = lexer.analyze()
        
        # Store the tokens for synchronization purposes
        self.current_tokens = tokens
        
        # Populate the results table
        self._populate_results_table(tokens)
        
        if hasattr(self, 'status_bar') and self.status_bar:
            try:
                self.status_bar.showMessage(f"Análisis completado: {len(tokens)} tokens encontrados")
            except AttributeError:
                print(f"Análisis completado: {len(tokens)} tokens encontrados")
        
        # Highlight the current line in the source code editor
        self._highlight_current_line()

    def _populate_results_table(self, tokens: list[Token]) -> None:
        """Populate the results table with the analyzed tokens."""
        # Get the current tab to access the UI elements
        current_tab = self.workspace.currentWidget()
        if not current_tab:
            return

        results_view = None
        if hasattr(current_tab, 'results_view'):
            results_view = current_tab.results_view
        else:
            try:
                view_widget = current_tab.widget()
                if view_widget and hasattr(view_widget, 'results_view'):
                    results_view = view_widget.results_view
            except AttributeError:
                pass

        if not results_view:
            return

        # Clear existing rows
        results_view.setRowCount(0)
        
        # Define colors for different token types (Catppuccin colors)
        token_colors = {
            "INSTRUCCIÓN": "#cba6f7",      # mauve
            "REGISTRO": "#fab387",          # peach
            "TIPO_DATO": "#89dceb",         # sky
            "CONSTANTE_HEX": "#a6e3a1",     # green
            "CONSTANTE_BIN": "#a6e3a1",     # green
            "CONSTANTE_DEC": "#a6e3a1",     # green
            "CONSTANTE_STR": "#a6e3a1",     # green
            "PSEUDOINSTRUCCIÓN": "#89b4fa", # blue
            "SÍMBOLO": "#f38ba8",           # red
            "SEPARADOR": "#f5c2e7",         # pink
            "OPERADOR_COMPUESTO": "#f9e2af" # yellow
        }
        
        # Add tokens to the table
        for row, token in enumerate(tokens):
            results_view.setRowCount(row + 1)
            
            # Column 0: Token number
            num_item = QTableWidgetItem(str(row + 1))
            num_item.setFlags(num_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            results_view.setItem(row, 0, num_item)
            
            # Column 1: Token value
            value_item = QTableWidgetItem(token.value)
            value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            results_view.setItem(row, 1, value_item)
            
            # Column 2: Token type
            type_item = QTableWidgetItem(token.type)
            type_item.setFlags(type_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            
            # Set color based on token type
            if token.type in token_colors:
                from PyQt6.QtGui import QColor
                color = QColor(token_colors[token.type])
                type_item.setForeground(color)
            
            results_view.setItem(row, 2, type_item)
    
    def _add_default_table_data(self) -> None:
        """Add some default data to the table for testing purposes."""
        current_tab = self.workspace.currentWidget()
        if not current_tab:
            return

        results_view = None
        if hasattr(current_tab, 'results_view'):
            results_view = current_tab.results_view
        else:
            try:
                view_widget = current_tab.widget()
                if view_widget and hasattr(view_widget, 'results_view'):
                    results_view = view_widget.results_view
            except AttributeError:
                pass

        if not results_view:
            return

        # Clear any existing rows
        results_view.setRowCount(0)
        
        # Add some default sample data 
        sample_tokens = [
            (1, "MOV", "INSTRUCCIÓN"),
            (1, "AX", "REGISTRO"), 
            (1, ",", "SEPARADOR"),
            (1, "@DATA", "SÍMBOLO"),
            (2, "LEA", "INSTRUCCIÓN"),
            (2, "DX", "REGISTRO"),
            (2, ",", "SEPARADOR"),
            (2, "msg", "SÍMBOLO"),
        ]
        
        # Define colors for different token types (Catppuccin colors)
        token_colors = {
            "INSTRUCCIÓN": "#cba6f7",      # mauve
            "REGISTRO": "#fab387",          # peach
            "TIPO_DATO": "#89dceb",         # sky
            "CONSTANTE_HEX": "#a6e3a1",     # green
            "CONSTANTE_BIN": "#a6e3a1",     # green
            "CONSTANTE_DEC": "#a6e3a1",     # green
            "CONSTANTE_STR": "#a6e3a1",     # green
            "PSEUDOINSTRUCCIÓN": "#89b4fa", # blue
            "SÍMBOLO": "#f38ba8",           # red
            "SEPARADOR": "#f5c2e7",         # pink
            "OPERADOR_COMPUESTO": "#f9e2af" # yellow
        }
        
        for row, (line_num, value, token_type) in enumerate(sample_tokens):
            results_view.setRowCount(row + 1)
            
            # Column 0: Token number
            num_item = QTableWidgetItem(str(row + 1))
            num_item.setFlags(num_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            results_view.setItem(row, 0, num_item)
            
            # Column 1: Token value
            value_item = QTableWidgetItem(value)
            value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            results_view.setItem(row, 1, value_item)
            
            # Column 2: Token type
            type_item = QTableWidgetItem(token_type)
            type_item.setFlags(type_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            
            # Set color based on token type
            if token_type in token_colors:
                from PyQt6.QtGui import QColor
                color = QColor(token_colors[token_type])
                type_item.setForeground(color)
            
            results_view.setItem(row, 2, type_item)