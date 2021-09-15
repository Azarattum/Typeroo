from PySide6.QtCore import *
from PySide6.QtWidgets import *


class MovableLabel(QLabel):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.parent = parent
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.parent.press_control == 0:
                self.pos = e.pos()
                self.main_pos = self.parent.pos()

        super().mousePressEvent(e)
        QPoint().x()

    def mouseMoveEvent(self, e):
        if self.parent.cursor().shape() == Qt.ArrowCursor:
            self.last_pos = e.pos() - self.pos
            self.main_pos += self.last_pos
            self.parent.move(self.main_pos)
        super(MovableLabel, self).mouseMoveEvent(e)


class Header(QWidget):
    def __init__(self, window):
        super().__init__()
        title = MovableLabel("Typeroo", window)
        close = QPushButton("X")
        close.clicked.connect(window.hide)

        grid = QGridLayout()
        grid.addWidget(title, 0, 0)
        grid.addWidget(close, 0, 1, Qt.AlignRight)

        self.setLayout(grid)
