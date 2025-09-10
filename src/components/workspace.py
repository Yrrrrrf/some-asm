# standard imports
from dataclasses import dataclass

# third-party imports
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

# local imports
from config.globals import Assets
from components.vistualizer import Visualizer
from components.code_editor import CodeEditor


@dataclass
class Workspace(QTabWidget):
    '''
    The workspace is the container of the visualizer.

    It handles the mouse events and the buttons of the visualizer.

    Also it handles the buttons of the image buffer's. (RUD operations)
    '''
    v_list: list[Visualizer]  # * list of visualizers (One for each tab)


    def __init__(self):
        super().__init__()
        self.setProperty('class', 'workspace')
        self.setMovable(True)
        # self.setMouseTracking(True)

        # * New Tab button
        add_button = QPushButton()
        add_button.clicked.connect(self._new_tab)
        add_button.setProperty('class', 'add_button')
        self.setCornerWidget(add_button, Qt.Corner.TopRightCorner)

        # * Close Tab button
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self._close_tab)

        # * Set initial tabs
        self.v_list = []  # * list of visualizers (One for each tab)
        [self._new_tab() for _ in range(1)]  # Create n tabs (n: int)

        # print(self.v_list)

        # V is a Visualizer
        # -> parent: QWidget: some_widget
        # -> parent: QScrollArea: scroll_area
        # -> parent: QStackedWidget
        # -> parent: Workspace (self)
        # for v in self.v_list:
            # print(type(v))


    def _new_tab(self):
        '''
        Create a new tab with a visualizer.
        Also set the buttons of the image buffer's inside the visualizer.
        '''
        # * Instantiate the visualizer, the scroll zone & the scroll area
        some_widget = QWidget()
        some_widget.setProperty('class', 'some_widget')
        some_widget.setLayout(QHBoxLayout())

        visualizer = Visualizer(some_widget)
        v2 = CodeEditor(some_widget)
        
        # * Add the visualizer to the scroll area
        some_widget.layout().addWidget(visualizer)
        some_widget.layout().addWidget(v2)
        
        # * Add the scroll area to the tab widget
        self.addTab(some_widget, f'New_{self.count()+1}')

        # * Add the visualizer to the list of visualizers
        self.v_list.append(visualizer)


    def _close_tab(self, index: int):
        """
        Close the tab at the given index.

        If the last tab is closed, create a new one. This is to avoid having no tabs.

        ## Arguments:
            - index (int): the index of the tab to close
        """
        # TODO: Add a confirmation dialog (are you sure you want to close this tab?)
        self.removeTab(index)   # Remove the tab from the tab widget
        self.v_list.pop(index)  # * Remove the visualizer from the list of visualizers
        if self.count() == 0: self._new_tab()  # If there are no tabs, create a new one
