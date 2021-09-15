from platform import platform
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from BlurWindow.blurWindow import GlobalBlur


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.press_control = 0
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        pixmap = QPixmap("assets/icon.svg")
        self.setWindowIcon(QIcon(pixmap))
        self.setWindowTitle(str())

        self.setMinimumSize(350, 400)
        self.setMaximumWidth(350)

        palette = QPalette()
        palette.setColor(QPalette.Text, QColor(0, 180, 0))
        palette.setColor(QPalette.PlaceholderText, QColor(180, 0, 0))
        self.setPalette(palette)

        GlobalBlur(self.winId(), Dark=True, Acrylic=True, QWidget=self)
        with open("style.qss", "r") as style:
            self.setStyleSheet(style.read())
