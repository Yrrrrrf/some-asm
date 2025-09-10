"""
Some Assembly

This is the main file of the application. It is responsible for setting up the logging system and configuring it.

Author: Yrrrrrf
"""


# standard imports
from sys import exit, argv

# third-party imports
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# local imports
from components.loading_screen import LoadingScreen
from config.globals import Config
from components.app import App

from some_asm import hello
    
def main() -> None:
    """
    Application entry point. 

    It is also responsible for setting up the logging system and configuring it.
    """
    app = QApplication(argv)  # Manage the GUI application's control flow and main settings.
    main_window = App()  # Create the instance of the MainWindow

    # show_loading_screen = True
    show_loading_screen = False
    match show_loading_screen:
        case True:
            loading_screen = LoadingScreen()
            loading_screen.show()
            QTimer.singleShot(2000, loading_screen.close)  # Execute the main_window.show() function after 2 seconds
            QTimer.singleShot(2000, main_window.show)  # Execute the main_window.show() function after 2 seconds
        case False: main_window.show()  # Show the main window
    exit(app.exec())  # Execute the app


if __name__ == "__main__":
    """
    This is the entry point of the application.
    Clean the terminal and print app data before running the main function.
    Then run the main function.
    """
    print("\033[2J\033[1;1H", end="")  # clear terminal
    print(f"\033[92m{Config.NAME.value}\033[0m", end=" ")  # print n puzzle solver in green
    print(f"\033[97m{Config.VERSION.value}\033[0m")  # print version in white
    print(f"Author(s): \033[94m{Config.AUTHOR.value}\033[0m", end="\n\n")  # print author in blue

    print(hello())
    main()  # run main function
