import sys
import code
from io import StringIO

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from spyderlib.widgets import internalshell


class ManiWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ManiWindow, self).__init__(parent)

        layout = QHBoxLayout()
        bar = self.menuBar()
        file = bar.addMenu("&File")
        # file.addAction("Save")

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
        self.dock.setWidget(self.pythonshell)
        self.dock.setFloating(False)
        self.setCentralWidget(QTextEdit())
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.setLayout(layout)
        self.setWindowTitle("Dock demo")

    def __add_line(self, str):
        postfix = ''
        if str.rfind('\n') == -1:
            postfix = '\n'
        self.pythonshell.insert_text(str + postfix)
        self.pythonshell.run_command(str)

    def my_process(self):
        self.setWindowTitle("Hello!")
        cmd = "print('hello')"
        self.__add_line(cmd)
    


def main():
    app = QApplication(sys.argv)
    ex = ManiWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
