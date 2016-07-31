import sys
import code
from io import StringIO

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from spyderlib.widgets import internalshell

from OCC import VERSION
from OCC.Display.backend import load_backend, load_pyqt4, PYQT4
load_backend(PYQT4)
load_pyqt4()
from OCC.Display.qtDisplay import *
from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox

class ManiWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ManiWindow, self).__init__(parent)
        self.canva = qtViewer3d(self)
        self.setWindowTitle("pythonOCC-%s 3d viewer" % VERSION)
        self.canva.InitDriver()
        self.display = self.canva._display

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
        self.pythonshell = internalshell.InternalShell(self.dock, namespace=globals(), commands=[])
        self.pythonshell.interpreter.locals["self"] = self
        self.pythonshell.interpreter.locals["display"] = self.display
        self.dock.setWidget(self.pythonshell)
        self.dock.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.setCentralWidget(self.canva)
        self.resize(800, 600)

    def __add_line(self, str):
        postfix = ''
        if str.rfind('\n') == -1:
            postfix = '\n'
        self.pythonshell.insert_text(str + postfix)
        self.pythonshell.run_command(str)

    def my_process(self):
        # my_box = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()
        # self.display.DisplayShape(my_box, update=True)
        # cmd = "print('hello')"
        # self.__add_line(cmd)
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
