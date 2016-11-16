# -*- coding: utf-8 -*-
from qtpy.QtWidgets import QApplication, QAction, qApp, QMainWindow
from qtpy.QtGui import QIcon

from OCC import VERSION
from OCC.Display.backend import load_backend, load_pyqt5, PYQT5

load_backend(PYQT5)
load_pyqt5()
from OCC.Display.qtDisplay import *


class ManiWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ManiWindow, self).__init__(parent)
        # self.canvas = qtViewer3d(self)
        self.setWindowTitle("pythonOCC-%s 3d viewer" % VERSION)
        # self.canvas.InitDriver()

        bar = self.menuBar()
        file = bar.addMenu("&File")

        _new = QAction(QIcon('icons/exit.png'), '&New', self)
        _new.setStatusTip("New application")
        _new.triggered.connect(self.my_process)
        # self.connect(_new, SIGNAL("triggered()"), self.my_process)
        file.addAction(_new)

        _exit = QAction(QIcon('icons/exit.png'), '&Exit', self)
        _exit.setShortcut('Ctrl+Q')
        _exit.setStatusTip('Exit application')
        _exit.triggered.connect(qApp.quit)
        file.addAction(_exit)
        self.statusBar()

    def my_process(self):
        print('hello')
        pass


def main():
    app = QApplication(sys.argv)
    win = ManiWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
