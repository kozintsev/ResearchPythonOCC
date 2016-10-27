from PyQt4.QtCore import *
from PyQt4.QtGui import *
from spyder.widgets import internalshell

from OCC import VERSION
from OCC.Display.backend import load_backend, load_pyqt4, PYQT4

load_backend(PYQT4)
load_pyqt4()
from OCC.Display.qtDisplay import *


class ManiWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ManiWindow, self).__init__(parent)
        self.canvas = qtViewer3d(self)
        self.setWindowTitle("pythonOCC-%s 3d viewer" % VERSION)
        self.canvas.InitDriver()
        self.display = self.canvas._display

        bar = self.menuBar()
        file = bar.addMenu("&File")

        _new = QAction(QIcon('icons/exit.png'), '&New', self)
        _new.setStatusTip("New application")
        self.connect(_new, SIGNAL("triggered()"), self.my_process)
        file.addAction(_new)

        _exit = QAction(QIcon('icons/exit.png'), '&Exit', self)
        _exit.setShortcut('Ctrl+Q')
        _exit.setStatusTip('Exit application')
        self.connect(_exit, SIGNAL('triggered()'), SLOT('close()'))
        file.addAction(_exit)
        self.statusBar()

        self.dock = QDockWidget("Python Shell", self)
        self.python_shell = internalshell.InternalShell(self.dock, namespace=globals(), commands=[])
        self.python_shell.interpreter.locals["self"] = self
        self.python_shell.interpreter.locals["display"] = self.display
        self.dock.setWidget(self.python_shell)
        self.dock.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.setCentralWidget(self.canvas)
        self.resize(800, 600)

    def __add_line(self, command):
        postfix = ''
        if command.rfind('\n') == -1:
            postfix = '\n'
        self.python_shell.insert_text(command + postfix, at_end=True)
        self.python_shell.keyPressEvent()
        #self.python_shell.on_enter(command)
        #self.python_shell.flush()


    def my_process(self):
        cmd = "from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox"
        self.__add_line(cmd)
        cmd = "my_box = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()"
        self.__add_line(cmd)
        cmd = "self.display.DisplayShape(my_box, update=True)"
        self.__add_line(cmd)


def main():
    app = QApplication(sys.argv)
    win = ManiWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
