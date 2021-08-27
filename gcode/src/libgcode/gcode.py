from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QTextCharFormat
from PyQt5.QtCore import Qt

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
	fmt.setUnderlineColor(Qt.red)
	fmt.setUnderlineStyle(QTextCharFormat.SingleUnderline)
	#fmt.setUnderlineStyle(QTextCharFormat.DashUnderline)
	#fmt.setUnderlineStyle(QTextCharFormat.DotLine)
	#fmt.setUnderlineStyle(QTextCharFormat.DashDotLine)
	#fmt.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
	#fmt.setUnderlineStyle(QTextCharFormat.WaveUnderline)
	cursor = parent.gcodePTE.textCursor()
	position = cursor.position()
	cursor.select(QTextCursor.Document)
	cursor.setCharFormat(QTextCharFormat())
	cursor.clearSelection()
	cursor.setPosition(position)
	cursor.select(QTextCursor.LineUnderCursor)
	cursor.setCharFormat(fmt)
