def interpret():
	
	# Embedding a Python interpreter!
	
	import sys
	import code
	from io import StringIO

	from PyQt4.QtCore import QObject, QString, pyqtSignal
	from PyQt4.QtGui import QWidget, QGridLayout, QTextEdit, QLineEdit, QLabel

	# TODO: colour text based on stderr/stdout
	#       print input text alongside output (different colour?)
	class Interpreter(QObject, code.InteractiveConsole):
		output = pyqtSignal(QString)

		def __init__(self):
			QObject.__init__(self)
			self.l = {}
			code.InteractiveConsole.__init__(self, self.l)
			self.out = StringIO()

		def write(self, data):
			self.output.emit(data)

		def runcode(self, codez):
			"""
			Reimplementation to capture stdout and stderr
			"""
			sys.stdout = self.out
			sys.stderr = self.out
			result = code.InteractiveConsole.runcode(self, codez)
			sys.stdout = sys.__stdout__
			sys.stderr = sys.__stderr__
			self.output.emit(self.out.getvalue())
			return result


	wid = QWidget()
	layout = QGridLayout(wid)

	display = QTextEdit()
	display.setReadOnly(True)
	layout.addWidget(display, 0,0, 1,2)

	prompt = QLabel(">>>")
	layout.addWidget(prompt, 1,0)

	input = QLineEdit()
	layout.addWidget(input, 1,1)

	interp = Interpreter()

	def text_input():
		text = input.text()
		input.clear()

		if interp.push(str(text)):
			# More input required
			# Use sys.ps1 and sys.ps2
			prompt.setText("...")
		else:
			prompt.setText(">>>")

	input.returnPressed.connect(text_input)
	
	def text_output(text):
		display.setPlainText(text)
		#display.append(text)
	
	interp.output.connect(text_output)

	wid.show()
	sys.exit(app.exec_())