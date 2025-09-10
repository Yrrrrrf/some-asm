# standard imports
from dataclasses import dataclass
import sys

# third-party imports
from PyQt6.QtWidgets import QApplication, QFrame, QProgressBar, QLabel
from PyQt6.QtGui import QImage, QFont, QPixmap
from PyQt6.QtCore import Qt, QTimer

# local imports
from config.globals import Assets

@dataclass
class LoadingScreen(QFrame):
    '''
    A progress bar with a custom style
    '''
    timer: QTimer
    title_bar: QLabel
    progress_bar: QProgressBar
    progress: int = 0


    def __init__(self):
        super().__init__()
        self.setProperty('class', 'loading_screen')
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(420, 256)

        self.set_image(f'{Assets.ICONS.value}philosophers-stone.png')
        self.set_title_bar()
        self.set_progress_bar()

        # set the timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(20)


    def set_image(self, path: str, x: int = 82, y: int = 0) -> None:
        '''
        Set one image in the loading screen at the given position
        '''
        icon_label = QLabel(self)
        icon_label.move(x, y)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setPixmap(
            QPixmap.fromImage(
                QImage(path).scaled(256, 256, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            )
        )


    def set_title_bar(self) -> None:
        '''
        Set the title bar of the loading screen
        '''
        self.title_bar = QLabel(self)
        self.title_bar.setFont(QFont('Segoe Print', 64, QFont.Weight.Bold))
        self.title_bar.setGeometry(0, 0, 420, 240)
        self.title_bar.setText('Canvas')

        # Create another QLabel a little bit smaller to create a border effect
        self.title_bar_border = QLabel(self)
        self.title_bar_border.setFont(QFont('Segoe Print', 72, QFont.Weight.Bold))
        self.title_bar.setStyleSheet('QLabel {color: #FFD700;}')
        self.title_bar_border.setGeometry(0, 0, 420, 240)
        self.title_bar_border.setText('Canvas')

        # set the alignment of the title bar
        self.title_bar_border.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)


    def set_progress_bar(self):
        # ? Set progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setProperty('class', 'loading_bar')
        self.progress_bar.setGeometry(60, 180, 300, 32)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setFont(QFont('Segoe Print', 10, QFont.Weight.Bold))
        self.progress_bar.setStyleSheet('QProgressBar {border: 1px solid #FFD700; border-radius: 10px; text-align: center;} QProgressBar::chunk {background-color: #FFD700;}')


    def loading(self):
        if self.progress < 100:
            self.progress += 1
            self.progress_bar.setValue(self.progress)
        else:
            self.close()

