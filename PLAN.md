### Visión General y Estrategia

1.  **Separación de Cuerpos (Decoupling):** Mantendremos la lógica del analizador léxico (`core`) completamente separada de la interfaz gráfica (`ui`). El `core` no sabrá que existe PyQt6; solo tomará texto y devolverá una estructura de datos (una lista de tokens). Esto es crucial para la mantenibilidad y las pruebas.
2.  **Aprovechar `qt-ingot`:** Usaremos `IngotApp` como nuestra ventana principal. El `ActionManager` definirá nuestras acciones ("Abrir", "Analizar"), el `Display` organizará los paneles, el `SceneWorkspace` (aunque diseñado para escenas, su sistema de pestañas es útil) contendrá los espacios de trabajo de análisis y el `ThemeManager` le dará un aspecto profesional desde el primer día.
3.  **Desarrollo Incremental:** Construiremos la aplicación por fases, asegurando que cada componente funcione antes de integrarlo. Empezaremos con la lógica pura, luego construiremos el esqueleto de la UI y finalmente los conectaremos.

---

### Plan de Desarrollo Detallado

#### **Fase 0: Estructura y Configuración del Proyecto**

*Objetivo: Preparar el terreno para un desarrollo limpio y organizado.*

1.  **Crear la Estructura de Directorios:**
    ```
    tu-ensamblador/
    ├── src/
    │   ├── core/
    │   │   ├── __init__.py
    │   │   └── lexer.py         # Aquí vivirá la lógica del analizador léxico.
    │   ├── ui/
    │   │   ├── __init__.py
    │   │   └── main_window.py   # Definirá nuestra ventana principal, heredando de IngotApp.
    │   └── main.py              # Punto de entrada de la aplicación.
    ├── resources/
    │   └── (iconos, etc.)
    └── pyproject.toml           # Gestionará las dependencias.
    ```
2.  **Configurar Dependencias:** (completo!)

3.  **Crear Placeholders:** Crea los archivos `lexer.py` y `main_window.py` con clases vacías para empezar.

#### **Fase 1: El Cerebro - Lógica del Analizador Léxico (en `src/core/`)**

*Objetivo: Construir y probar un `Lexer` robusto que funcione independientemente de la GUI.*

1.  **Definir la Estructura del Token:** En `lexer.py`, define una estructura de datos para los tokens. Una `dataclass` es ideal para esto.
O mejor aun! Utiliza pydantic para mayor robustez!
    ```python
    from pydantic import BaseModel

    class Token(BaseModel):
        value: str
        type: str
        line: int
    ```
2.  **Definir los Diccionarios de Elementos:** Crea `sets` (conjuntos) para una búsqueda ultra-rápida de instrucciones, registros y pseudoinstrucciones.
    ```python
    INSTRUCTIONS = {"AAA", "AAD", "HLT", ...} # Las de la imagen
    REGISTERS = {"AX", "BX", "CX", "DX", "AL", "AH", ...}
    # ... etc.
    ```
3.  **Implementar la Clase `Lexer`:**
    *   El `__init__` recibirá el código fuente como una sola cadena de texto.
    *   Un método privado `_clean_code()` eliminará los comentarios.
    *   Un método privado `_tokenize()` se encargará de la lógica de separación. **Este es el paso más complejo.** Debe:
        *   Manejar los separadores (`espacio`, `,`, `:`).
        *   Tener lógica especial para no separar los **elementos compuestos** (`.data segment`, `byte ptr`, `[xxx]`, `"xxx"`). Una estrategia es usar una máquina de estados o una pasada de pre-procesamiento para reemplazar temporalmente estos compuestos antes de la separación principal.
    *   Un método privado `_classify(token_value: str) -> str` recibirá un token (una cadena) y devolverá su tipo (`INSTRUCCIÓN`, `SÍMBOLO`, `CONSTANTE_HEX`, etc.). Aquí usarás los `sets` definidos antes.
    *   Un método público `analyze() -> list[Token]` orquestará todo el proceso y devolverá la lista final de tokens clasificados.

4.  **Probar desde la Terminal:** Crea un pequeño script (`if __name__ == "__main__":`) dentro de `lexer.py` que lea uno de los archivos de ejemplo de `some-asm`, se lo pase al `Lexer` y imprima el resultado en la consola. **Esto te permite depurar el 90% de la lógica del proyecto sin tocar la GUI.**

5. Crear una herramienta de CLI que tenga un output más amigable (ej. tabla con colores usando `rich`) que permita analizar archivos desde la terminal! Este mismo script puede ser el punto de entrada para pruebas rápidas y posterior integración con la GUI!!! :D

#### **Fase 2: El Esqueleto - La Interfaz Gráfica (en `src/ui/`)**

*Objetivo: Usar `qt-ingot` para montar una interfaz funcional sin la lógica de análisis todavía.*

1.  **Crear la Ventana Principal (`main_window.py`):**
    *   Define una clase `MainWindow` que herede de `ingot.app.IngotApp`.
    *   En el `__init__`, configura el título y el ícono usando el `config` de `IngotApp`.
    *   **Define la Estructura del Menú:** Crea el diccionario para el `ActionManager` con las acciones "Abrir Archivo..." y "Analizar".
        ```python
        MENU_CONFIG = {
            "Archivo": [
                {"name": "Abrir Archivo...", "shortcut": "Ctrl+O", "function": self.open_file_dialog},
                {"name": "Exit", "shortcut": "Esc", "function": sys.exit}
            ],
            "Análisis": [
                {"name": "Analizar Código", "shortcut": "F5", "function": self.analyze_code}
            ]
        }
        self.set_menu(MENU_CONFIG)
        ```
    *   **Crear el Widget Central:** El corazón de tu UI será un `QSplitter` para tener dos paneles redimensionables.
        ```python
        from PyQt6.QtWidgets import QSplitter, QTextEdit, QTableWidget, QHeaderView

        central_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Panel izquierdo para el código fuente
        self.source_code_view = QTextEdit()
        self.source_code_view.setPlaceholderText("Abre un archivo .asm para empezar...")

        # Panel derecho para los resultados (una tabla es mejor que texto plano)
        self.results_view = QTableWidget()
        self.results_view.setColumnCount(3)
        self.results_view.setHorizontalHeaderLabels(["#", "Elemento", "Tipo"])
        self.results_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # Columna "Elemento" se estira

        central_splitter.addWidget(self.source_code_view)
        central_splitter.addWidget(self.results_view)
        ```
    *   **Integrar con `qt-ingot`:** `qt-ingot` usa un sistema de pestañas. Colocaremos nuestro `QSplitter` dentro de la primera pestaña.
        ```python
        # Obtenemos la primera pestaña creada por defecto por SceneWorkspace
        first_tab = self.workspace.widget(0)
        # Reemplazamos su contenido por nuestro splitter
        first_tab.setWidget(central_splitter)
        self.workspace.setTabText(0, "Análisis Léxico")
        ```
    *   Implementa los métodos `open_file_dialog` y `analyze_code` como placeholders (ej. que solo hagan `print("Función no implementada")`).

2.  **Configurar `main.py`:**
    ```python
    import sys
    from PyQt6.QtWidgets import QApplication
    from ui.main_window import MainWindow

    def main():
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

    if __name__ == "__main__":
        main()
    ```

**¡Hito 2!** En este punto, deberías poder ejecutar tu programa, ver una ventana con dos paneles vacíos y un menú funcional (aunque los botones no hagan nada útil todavía).

#### **Fase 3: La Conexión - Integración Lógica y UI**

*Objetivo: Hacer que la UI use el Lexer para mostrar resultados reales.*

1.  **Implementar `open_file_dialog`:**
    *   Usa `QFileDialog` para obtener la ruta de un archivo.
    *   Valida que el archivo exista.
    *   Lee el contenido y colócalo en `self.source_code_view`.
    *   Usa el status bar de `qt-ingot` para mostrar un mensaje: `self.status_bar.showMessage(f"Archivo cargado: {filename}")`.
2.  **Implementar `analyze_code`:**
    *   Obtén el texto de `self.source_code_view`.
    *   Crea una instancia de tu clase `Lexer` con ese texto.
    *   Llama a `lexer.analyze()` para obtener la `list[Token]`.
    *   Llama a un nuevo método `_populate_results_table(tokens)` para mostrar los datos.
3.  **Implementar `_populate_results_table`:**
    *   Limpia la tabla de resultados (`self.results_view.setRowCount(0)`).
    *   Itera sobre la lista de tokens. Por cada token:
        *   Inserta una nueva fila en la tabla.
        *   Crea `QTableWidgetItem` para el número de línea, el valor del token y el tipo de token.
        *   Añade los items a la fila.
    *   Usa el status bar para mostrar un resumen: `self.status_bar.showMessage(f"Análisis completado. {len(tokens)} elementos encontrados.")`.

#### **Fase 4: Refinamiento y Paginación**

*Objetivo: Cumplir con los requisitos finales y mejorar la experiencia de usuario.*

1.  **Implementar Paginación:** El requisito de paginación es importante.
    *   Modifica `_populate_results_table` para que acepte un `page_number`.
    *   Almacena la lista completa de tokens en una variable de la clase (ej. `self.all_tokens`).
    *   Calcula el `slice` de la lista que corresponde a la página actual (ej. `tokens[start_index:end_index]`).
    *   Añade botones "Anterior" y "Siguiente" a la UI (pueden ir en un `QWidget` debajo de la tabla de resultados).
    *   Conecta estos botones para que modifiquen el número de página actual y vuelvan a llamar a `_populate_results_table`.
2.  **Mejoras de Estilo:**
    *   Crea un archivo `theme.scss` personalizado para tu proyecto y cárgalo con el `ThemeManager` de `qt-ingot`. Puedes darle colores específicos a los tipos de tokens en la tabla.
3.  **Pulido Final:** Asegúrate de que todos los requisitos del proyecto original se cumplan, como los mensajes de error para elementos no identificados.

Este plan te da una ruta clara, modular y profesional para construir tu ensamblador, aprovechando al máximo el excelente trabajo que ya hiciste con `qt-ingot`. ¡Mucho éxito