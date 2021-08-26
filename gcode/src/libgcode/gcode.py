from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QTextCharFormat

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

def selectLine(parent):
	#print('here')
	fmt = QTextCharFormat()
	#fmt.setUnderlineColor(Qt.red)
	fmt.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
	cursor = parent.gcodePTE.textCursor()
	cursor.select(QTextCursor.LineUnderCursor)
	cursor.setCharFormat(fmt)
