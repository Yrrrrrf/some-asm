# standard imports
from dataclasses import dataclass
from functools import (
    partial,
)  # ? To pass arguments to a function in a lambda expression

# third-party imports
from PyQt6.QtWidgets import QFrame, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

# local imports
from config.globals import Assets


@dataclass
class SidePanel(QFrame):  # QWidget, but temporary is a QFrame just for testing
    """
    Side Bar contains the tools and the settings of the application.
    """

    margin: int = 8  # margin between the buttons
    buttons_size: int = 48  # default size of the buttons
    is_expanded: bool = False  # Flag to track the toggle state

    def __init__(self):
        super().__init__()
        self.setProperty("class", "side_panel")
        self.setMinimumWidth(
            self.margin * 2 + self.buttons_size
        )  # set the initial size of the side bar (not expanded)

        for i in range(5):
            s = SPButton(
                self,
                "gallery",
                [{"name": "Some", "fn": partial(lambda i: print(f"Some_{i}"), i)}],
            )
            s.move(self.margin, self.margin + (i * (self.buttons_size + self.margin)))

    def mousePressEvent(self, event):
        """
        When the mouse is pressed, the side bar will expand or collapse.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            match self.is_expanded:
                case True:
                    self.setFixedWidth(self.margin * 2 + self.buttons_size)
                case False:
                    self.setFixedWidth(200)
            self.is_expanded = not self.is_expanded


@dataclass
class SPButton(QPushButton):
    """
    SideBarButton class contains a list of operations that can be executed to an image.
    Every operation is a button will appear in the Operations Menu.
    """

    side_panel: SidePanel  # ? Parent Widget
    operations: list[dict]  # ? list of operations

    def __init__(self, side_panel: SidePanel, name: str, operations: list[dict]):
        super().__init__(side_panel)
        self.operations = operations
        self.setProperty("class", "sidebar_button")
        self.setIcon(QIcon(Assets.ICONS.value + name.lower() + ".png"))
        self.setIconSize(
            QSize(
                (int)(side_panel.buttons_size * 0.8),
                (int)(side_panel.buttons_size * 0.8),
            )
        )
        self.setFixedSize(
            side_panel.buttons_size, side_panel.buttons_size
        )  # default size
        self.clicked.connect(
            self.operations[0]["fn"]
        )  # ? connect the button to the first operation


# @dataclass
# class OperationsMenu(QStackedWidget):
#     '''
#     Operations menu contains the operations that can be applied to the image.
#     These operations are displayed as buttons.
#     '''
#     side_panel: SidePanel
#     deployed: bool = False
#     showing_size = 240


#     def __init__(self, side_bar: SidePanel):
#         '''
#         Initialize the operations menu.
#         '''
#         super().__init__(side_bar)


# @dataclass
# class OperationButton(QPushButton):
#     '''
#     OperatoinButton class contains executes an operation to an image.
#     Every operation is a button. The button is a child of the operations frame.
#     If the unit test associated to the operation is passed, the button will be enabled.
#     '''
#     operations_menu: QWidget  # ? Parent Widget
#     # operation: dict  # contains the name and the function of the operation
#     icon: str
#     button_height: int = 32
#     icon_size: int = 24


#     def __init__(self, operations_menu: QWidget, operation: dict):
#         super().__init__(operations_menu)
#         self.name = operation['name']
#         self.operation = operation['function']
#         self.operations_menu = operations_menu
#         self.setFont(QFont('Segoe Print', 10, QFont.Weight.Bold))
#         # self.setIcon(QIcon(ICONS+icon))
#         self.setIconSize(QSize(self.icon_size, self.icon_size))
#         # self.setFixedSize(122, self.button_height)
#         self.setText(self.name)
#         self.setProperty('class', 'operation_button')

#         self.set_operation()


#     def set_operation(self) -> None:
#         '''
#         Set the operation of the button.
#         '''
#         pass
#         # path = 'resources\\img\\lena.png'
#         # self.clicked.connect(self.execute_operation)


#     def execute_operation(self) -> None:
#         '''
#         Execute the operation of the button.
#         Converts an array to a QImage and sets it as the active image.
#         Also sets the active image path.
#         '''
#         try:
#             from components.image_buffer import active_buffer, QImage, QPixmap
#             # global active_image_path
#             cv_image = cv.imread(active_buffer.image_path)
#             # apply the operation
#             # cv.imshow('image', cv_image)
#             cv_image = cv.cvtColor(cv_image, cv.COLOR_BGR2RGB)
#             cv_image = self.operation(cv_image)
#             print(f'Executing operation: {self.name}')
#             # cast it as a numpy ndarray
#             cv_image = np.ndarray(shape=(cv_image.shape[0], cv_image.shape[1], 3), dtype=np.uint8, buffer=cv_image.data, strides=(cv_image.strides[0], cv_image.strides[1], cv_image.strides[2]))
#             height, width, bytesPerComponent = cv_image.shape
#             bytesPerLine = bytesPerComponent*width
#             active_buffer.q_image = QImage(cv_image.data, width, height, bytesPerLine, QImage.Format.Format_RGB888)
#             active_buffer.setPixmap(QPixmap.fromImage(active_buffer.q_image))
#             # save the image
#             active_buffer.image_path = 'resources\\img\\temp\\edit.png'  # update image path
#             # img = cv.imwrite('resources\\img\\temp\\edit.png', cv_image., format=)  # save it in the temp directory
#             # save it in bgr format
#             cv_image = cv.cvtColor(cv_image, cv.COLOR_RGB2BGR)
#             cv.imwrite('resources\\img\\temp\\edit.png', cv_image)
#             # cv.imshow('image', img)

#             active_buffer.update()
#         except ImportError:
#             print('\nError: No image selected')


# from dataclasses import dataclass

# from components.operation_button import OperationButton
# from PyQt6.QtWidgets import QFrame, QLabel, QStackedWidget
# from PyQt6.QtGui import QFont
# from PyQt6.QtCore import Qt

# from globals import APP_COLOR


# @dataclass
# class OperationsPage(QFrame):
#     '''
#     Every page belongs to a OperationsMenu.
#     Is a page that contains the operations that can be applied to the image.
#     These operations are displayed as buttons.
#     '''
#     operations_menu: QStackedWidget  # ? Parent Widget
#     operations: list[dict]
#     deployed: bool = False  # ? Whether the operations menu is deployed or not
#     showing_size = 240  # ? The width of the operations menu when it is deployed


#     def __init__(self, operations_menu: QStackedWidget, title: str, operations: list[dict]):
#         '''
#         Initialize the operations page inside the operations menu.
#         The page contains a OperationButton for each operation.
#         '''
#         super().__init__(operations_menu)
#         self.operations_menu = operations_menu
#         self.operations = operations
#         self.title = QLabel(self)
#         self.title.setProperty('class', 'operations_page_title')
#         self.set_title(title)
#         self.set_operations()
#         self.setProperty('class', 'operations_page')


#     def set_title(self, title: str) -> None:
#         '''
#         Set the title of the operations menu.
#         Every time the title is changed, the title label is recentered.
#         '''
#         from components.side_bar import SideBar, SideBarButton
#         self.title.setText(title)
#         self.title.setFont(QFont('Segoe Print', 16, QFont.Weight.Bold))
#         self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.title.setGeometry(SideBar.margin*4, SideBar.margin*2, self.showing_size-SideBar.margin*8, SideBarButton.size-SideBar.margin)


#     def set_operations(self) -> None:
#         '''
#         Set the operations of the operations menu.
#         '''
#         from components.operation_button import OperationButton
#         from components.side_bar import SideBar, SideBarButton
#         ops_size = (int)(SideBarButton.size/2)

#         for i in range(len(self.operations)):
#             OperationButton(self, self.operations[i]) \
#             .setGeometry(SideBar.margin*2, self.title.height()+SideBar.margin*4+(i*(SideBar.margin+ops_size)), self.showing_size-SideBar.margin*4, ops_size)

#         self.setFixedHeight(self.title.height()+((1+len(self.operations))*(SideBar.margin+ops_size)))
