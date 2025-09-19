# standard imports
import sys

# third-party imports
from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction

# own imports
from config.globals import Config
from components.workspace import Workspace


class MenuBar(QMenuBar):
    """
    The MenuBar class represents the menu bar of the application.

    This class is a subclass of QMenuBar and contains the menus and options of the application.
    It sets the menu bar of the main window.
    """

    def __init__(self):
        """
        Initialize a new instance of MenuBar.
        """
        super().__init__()
        self.setProperty("class", "menu_bar")

        # * Define the elements of the Menu Bar
        self.menu_bar_dict = {
            "File": [
                {
                    "name": "Load Image",
                    "shortcut": "Ctrl+O",
                    # 'function': lambda: print('Load image function')
                },
                {
                    "name": "Remove Image",
                    "shortcut": "Ctrl+R",
                    # 'function': lambda: print('Save image function')
                },
                {
                    "name": "Save Image As",
                    "shortcut": "Ctrl+S",  # todo: check what is the shortcut for save as
                    # 'shortcut': 'Ctrl+Shift+S'
                    # 'function': lambda: print('Save image as function')
                },
                {"name": "Separator"},
                {
                    "name": "Exit",
                    "shortcut": "Esc",
                    "function": lambda: sys.exit(),  # exit the app
                },
            ],
            "View": [
                {
                    "name": "Zoom In",
                    "shortcut": "Ctrl++",
                },
                {
                    "name": "Zoom Out",
                    "shortcut": "Ctrl+-",
                },
                {"name": "Separator"},
                {
                    # todo: Create an emergent window to change the theme to the default ones or to a custom one
                    # todo: Create at least 3 themes: default, dark, dev
                    "name": "Change Theme",
                    "shortcut": "Ctrl+P",
                    "function": lambda: print("Still working on it...!"),
                },
            ],
            "Edit": [
                {
                    "name": "Undo",
                    "shortcut": "Ctrl+Z",
                    "function": lambda: print("Undo function"),
                },
                {
                    "name": "Redo",
                    "shortcut": "Ctrl+Y",
                    "function": lambda: print("ReDo function"),
                },
            ],
            "Help": [
                {
                    "name": "About",
                    "shortcut": "Ctrl+H",
                    "function": lambda: print(
                        f"[{Config.NAME.value}]\t\033[94m{Config.VERSION.value}\033[0m by \033[92m{Config.AUTHOR.value}\033[0m\thttps://github.com/Yrrrrrf/image_alchemy"
                    ),
                    # 'function': lambda: {
                    #     print(f'[{Config.NAME.value}]\t\033[94m{Config.VERSION.value}\033[0m by \033[92m{Config.AUTHOR.value}\033[0m', end='\t'),
                    #     print(f'https://github.com/Yrrrrrf/image_alchemy')  # Repo link
                    # }
                },
                {
                    "name": "Shortcut Keys",
                    "shortcut": "Ctrl+Shift+H",
                    # todo: Create a mini-window with all the shortcuts
                    "function": lambda: self._print_menu_bar(),
                },
            ],
        }

        # * Set the menu bar
        self.set_menu_bar()

    def set_menu_bar(self):
        """
        Set the menu bar by adding menus to it.

        This method iterates over the items in the `menu_bar_dict` dictionary.
        For each item, it creates a menu using the create_menu method and adds it to the menu bar.
        """
        for [menu_name, action_list] in self.menu_bar_dict.items():
            menu = QMenu(menu_name, self)
            menu.setProperty("class", "menu_bar_submenu")
            for action_dict in action_list:
                action = QAction(action_dict["name"], self)
                match action_dict["name"]:
                    case "Separator":
                        menu.addSeparator()
                    case _:
                        if "shortcut" in action_dict:
                            action.setShortcut(action_dict["shortcut"])
                        # if 'description' in action_dict: action.setStatusTip(action_dict['description'])
                        if "function" in action_dict:
                            action.triggered.connect(action_dict["function"])
                        menu.addAction(action)
            self.addMenu(menu)

    def _print_menu_bar(self):
        """
        Print the menu bar to the console
        """
        for menu in self.findChildren(QMenu):
            print(f"{menu.title()} {'=' * (40 - len(menu.title()))}")
            for action in menu.actions():
                print(f"\t{action.text():<20}{action.shortcut().toString()}")
            print("")
