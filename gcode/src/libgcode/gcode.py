from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QTextCursor

def copy(parent):
	qclip = QApplication.clipboard()
	qclip.setText(parent.gcodePTE.toPlainText())
	parent.statusbar.showMessage('G code copied to clipboard')

def delete(parent):
	cursor = parent.gcodePTE.textCursor()
	cursor.select(QTextCursor.LineUnderCursor)
	cursor.removeSelectedText()
	cursor.deleteChar()

def deleteAll(parent):
	parent.gcodePTE.clear()

def insert(parent):
	parent.gcodePTE.insertPlainText(parent.gcodeCustomLE.text())

def addM2(parent):
	parent.gcodePTE.appendPlainText('M2')
