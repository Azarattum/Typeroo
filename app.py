from BlurWindow.blurWindow import GlobalBlur
from storage import loadBindings
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from mappings import Mappings
from header import Header
from window import Window
from sys import argv
import time

app = QApplication(argv)
window = Window()

header = Header(window)
mappings = Mappings(window, app)

layout = QVBoxLayout()
layout.setContentsMargins(0, 0, 0, 0)
layout.addWidget(header)
layout.addWidget(mappings)

bindings = loadBindings()
for key, val in bindings:
    mappings.addItem(key, val)
mappings.addItem()

container = QWidget()
container.setLayout(layout)

menu = QMenu(window)
menu.setAttribute(Qt.WA_TranslucentBackground)
menu.setWindowFlags(menu.windowFlags() | Qt.FramelessWindowHint)
GlobalBlur(menu.winId(), Dark=True, Acrylic=True, QWidget=menu)
show = menu.addAction("&Typeroo")
quit = menu.addAction("&Quit")
show.triggered.connect(lambda: window.show() or window.activateWindow())
quit.triggered.connect(app.quit)

tray = QSystemTrayIcon()
tray.setIcon(QIcon("assets/icon.svg"))
tray.setVisible(True)
tray.setContextMenu(menu)

window.setCentralWidget(container)
window.show()
app.exec()
