# standard imports
from dataclasses import dataclass

# Third-party imports
import sass

from PyQt6.QtWidgets import QMainWindow, QMenu
from PyQt6.QtGui import QIcon, QAction, QKeySequence, QShortcut

# Own imports
from config.globals import *
from components.display import Display
from components.menu_bar import MenuBar


@dataclass
class App(QMainWindow):
    """
    App class
    This class contains the logic for the GUI
    """
    menu_bar: MenuBar
    display: Display


    def __init__(self):
        """
        Initialize the app
        """
        super().__init__()
        self.setProperty('class', 'app_window')  # set the class name for the stylesheet
        self.setWindowTitle(Config.NAME.value)
        self.setWindowIcon(QIcon(f"{Assets.ICONS.value}production.png"))
        self.setMinimumSize(Config.WIDTH.value, Config.HEIGHT.value)

        self.setMouseTracking(True)  # track mouse even when not clicking
        # self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # focus on the window

        self.menu_bar = MenuBar()
        self.setMenuBar(self.menu_bar)

        self.display = Display()
        self.setCentralWidget(self.display)


        # * Set the color scheme
        # todo: add some kind of Color Scheme Manager (like the Theme Manager)
        # self._set_color_scheme('default')

        # * Set a stylesheet for the app
        # todo: add some kind of Theme Manager (like the Color Scheme Manager)
        self._set_theme()
        # self._set_theme('main')  # empty for now...
        # self.setup_shortcuts()


        # * Assign the actions to the menu bar
        self.assign_actions()  # Set all the actions to their respective elements to apply the logic


    # def _set_color_scheme(self, schema: str = 'default'):
    #     """
    #     Load the stylesheet from the sass file

    #     # Arguments
    #         theme (str): the name of the theme to load

    #     # Theme names
    #         - `default`: the default theme
    #         - `dark`: the dark theme (not implemented yet)
    #         - `dev`: the development theme (not implemented yet)
    #     """
    #     with open(f"{Assets.THEMES.value}{schema}.scss", 'r') as file:
    #         self.setStyleSheet(compile(string=file.read()))



    def _set_theme(self, theme: str = 'dev'):
        """
        Load the stylesheet from the sass file based on the selected theme.

        Arguments:
            theme (str): the name of the theme to load, e.g., 'light' or 'dark'
        """
        try:
            with open(f"{Assets.THEMES.value}{theme}.scss", 'r') as file:
                self.setStyleSheet(sass.compile(string=file.read(),  # read the content of the file
                    include_paths=[
                        Assets.THEMES.value, 
                        Assets.COLOR_SCHEMA.value
                    ]  # set the include path
                ))
        except Exception as e:
            print(f"\033[31m{e}\x1B[37m")


    def assign_actions(self):
        """
        Assign the actions to the menu bar
        """
        # [print(menu.title()) for menu in self.menu_bar.findChildren(QMenu)]  # print the title of the menus
        # * Get the actions of the menu bar
        qactions = list(filter(lambda x: x.text() != "", self.menu_bar.findChildren(QAction)))
        # [print(action.text()) for action in qactions]  # print the text of the actions

        # * Add the behavior to the actions
        # open a new file
        qactions[1].triggered.connect(lambda: self.display.workspace.v_list[self.display.workspace.currentIndex()].open_file())
