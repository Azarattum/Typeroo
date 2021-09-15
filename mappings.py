from storage import setBinding, removeBinding
from BlurWindow.blurWindow import GlobalBlur
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
import keyboard


class Mappings(QScrollArea):
    map = dict()
    keys = dict()
    grid = QGridLayout()
    parent: QWidget
    app: QApplication
    animations = []

    def __init__(self, parent, app):
        self.app = app
        self.parent = parent
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

    def addItem(self, key=None, val=None):
        button = QPushButton(key or "&+")
        button.setContextMenuPolicy(Qt.CustomContextMenu)
        button.setMinimumWidth(109)

        edit = QLineEdit(val or "")
        edit.setAttribute(Qt.WA_TranslucentBackground)
        edit.setPlaceholderText("Output Sequence")
        if not val:
            edit.setMaximumWidth(0)

        button.clicked.connect(lambda: self.readHotkey(button))
        button.customContextMenuRequested.connect(
            lambda: self.openMenu(button))
        edit.textChanged.connect(lambda: (
            self.style().polish(edit)
        ))
        edit.editingFinished.connect(lambda: (
            self.updateMapping(button.text(), edit.text())
        ))

        self.map[button] = edit
        self.map[edit] = button

        row = self.grid.rowCount()
        self.grid.addWidget(button, row, 0, Qt.AlignTop)
        self.grid.addWidget(edit, row, 1, Qt.AlignTop)

        self.updateItems()
        self.ensureWidgetVisible(button)

        animation = QPropertyAnimation(button, b"maximumHeight")
        if not key:
            animation.setStartValue(0)
        animation.setEndValue(40)
        animation.start()
        animation.finished.connect(lambda: self.animations.remove(animation))
        self.animations.append(animation)

        if key and val:
            self.updateMapping(button.text(), edit.text())

    def removeItem(self, item):
        self.updateMapping(item.text(), None)

        effect = QGraphicsOpacityEffect(item)
        item.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setEndValue(0)
        animation.start()
        animation.finished.connect(lambda: {
            self.animations.remove(animation) or
            self.grid.removeWidget(item) or
            self.grid.removeWidget(self.map[item]) or
            self.updateItems()
        })
        self.animations.append(animation)

        effect = QGraphicsOpacityEffect(self.map[item])
        self.map[item].setGraphicsEffect(effect)
        animation2 = QPropertyAnimation(effect, b"opacity")
        animation2.setEndValue(0)
        animation2.start()
        animation2.finished.connect(lambda: {
            self.animations.remove(animation2)
        })
        self.animations.append(animation2)

    def updateItems(self):
        items = QWidget(self.parent)
        items.setLayout(self.grid)
        items.setMinimumWidth(self.parent.width() - 20)
        self.setWidget(items)

    def updateMapping(self, input, output):
        if input in self.keys:
            try:
                keyboard.remove_hotkey(self.keys[input])
            except:
                pass
            del self.keys[input]
            if not output or not input:
                removeBinding(input)
                return

        if not output or not input:
            self.keys[input] = None
            return

        self.keys[input] = keyboard.add_hotkey(
            input, lambda: keyboard.write(output),
            suppress=True
        )
        setBinding(input, output)

    def openMenu(self, sender):
        isEmpty = sender.text() == "&+"
        if isEmpty:
            return

        menu = QMenu("Menu", sender)
        remove = menu.addAction("&Remove")
        remove.triggered.connect(lambda: self.removeItem(sender))

        menu.setAttribute(Qt.WA_TranslucentBackground)
        menu.setWindowFlags(menu.windowFlags() | Qt.FramelessWindowHint)
        GlobalBlur(menu.winId(), Dark=True, Acrylic=True, QWidget=self)

        menu.exec(self.parent.cursor().pos())

    def readHotkey(self, sender):
        oldMapping = sender.text()
        isEmpty = sender.text() == "&+"

        sender.setText("Press a key...")
        self.app.processEvents()
        hotkey = keyboard.read_hotkey(suppress=False)
        if hotkey in self.keys.keys():
            sender.setText(oldMapping)
            return

        animation = QPropertyAnimation(self.map[sender], b"maximumWidth")
        animation.setEndValue(self.parent.width())
        animation.start()
        animation.finished.connect(lambda: self.animations.remove(animation))
        self.animations.append(animation)

        sender.setText(hotkey)
        self.app.processEvents()

        if not isEmpty and oldMapping in self.keys.keys():
            self.updateMapping(oldMapping, None)
        elif isEmpty:
            self.addItem()
        self.updateMapping(hotkey, self.map[sender].text())
