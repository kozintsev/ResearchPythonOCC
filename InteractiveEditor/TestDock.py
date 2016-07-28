import sys
import code
from io import StringIO

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from spyderlib.widgets import internalshell

class ManiWindow(QMainWindow):
   def __init__(self, parent = None):
      super(ManiWindow, self).__init__(parent)
		
      layout = QHBoxLayout()
      bar = self.menuBar()
      file = bar.addMenu("File")
      file.addAction("New")
      file.addAction("save")
      file.addAction("quit")
		
      self.dock = QDockWidget("Python Shell", self)
      self.pythonshell = internalshell.InternalShell(self.dock, namespace=globals(),commands=[])
      self.dock.setWidget(self.pythonshell)
      self.dock.setFloating(False)
      self.setCentralWidget(QTextEdit())
      self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
      self.setLayout(layout)
      self.setWindowTitle("Dock demo")
		
def main():
   app = QApplication(sys.argv)
   ex = ManiWindow()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()