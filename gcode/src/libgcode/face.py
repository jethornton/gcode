import os, configparser
from math import ceil
from PyQt5.QtWidgets import (QLineEdit, QSpinBox, QCheckBox, QComboBox,
	QLabel, QGroupBox, QDoubleSpinBox, QFileDialog, QMessageBox, QFileDialog)

#from PyQt5.QtWidgets import QMessageBox, QApplication, QFileDialog
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QTextCharFormat
from PyQt5.QtCore import Qt

from libgcode import files

def isnumber(i):
	try:
		tmp = float(i)
		return True
	except:
		return False

def retnumber(parent, i): # get line edit name then test for number
	if getattr(parent, i).text():
		try:
			num = float(getattr(parent, i).text())
			return round(num, 4)
		except Exception as e:
			print(e)
			name = getattr(parent, i).property("name")
			text = getattr(parent, i).text()
			print(i)
			parent.errorMsgOk(f'{name} {text} is not a number', 'Error')
			#print(f'{parent.faceWidthX.property("name")} is not a number')
			return False

def generate(parent):
	"""
	It is recommended that you program a tool path that keeps the milling cutter
	in full contact, rather than performing several parallel passes. When changing
	direction, include a small radial tool path to keep the cutter moving and
	constantly engaged

	start X face left - leadin
	cutter diamter / 2 is center 
	1" cutter 0.5" center -0.25" path is for 25%
	stepover cutter diameter * percent
	start Y = face rear minus cutter radius + step
	end X = width X + step * 2
	G2 arc X position + radius Y position - radius I0 J- radius
	X 9.5 
	X 9.5 + 0.5 Y-0.25 + 0.5 I0.0 jJ 9.5 - 0.5
	G2
	stock size decrease in size as cut
	
	initial cut path = radius - cutwidth
	I X offset relative
	J Y offset relative
	X10 Y5
	T5 M6 G43
	F25 S1800
	;leadin
	G0 X-0.5 Y0.1875
	1 G1 X10.0 Y0.1875
	2 G2 X10.1875 Y0.0 I0.0 J-0.1875
	3 G1 X10.1875 Y-5.0
	4 G2 X10.0 Y-5.1875 I-0.1875 J0.0
	5 G1 X0.0 Y-5.1875
	6 G2 X-0.1875 Y-5.0 I0.0 J0.1875
	7 G1 X-0.1875 Y-0.1875
	; second loop last positions - cutwidth
	8 G2 X0.0 Y0.0 I0.1875 J0.0
	"""
	parent.facePTE.clear()
	
	required = [
	'faceWidthX', 'faceDepthY', 'faceLeft', 'faceRear', 'faceRear',
	'faceTop', 'faceTool', 'faceToolDia', 'faceRPM', 'faceFeed',
	'faceSafeZ', 'faceLeadIn', 'faceFullDepth']
	error = False
	for item in required:
		if getattr(parent, item).text() == '':
			error = True
			name = getattr(parent, item).property('name')
			parent.facePTE.append(f'{name} is required')
	if error:
		return

	widthX = retnumber(parent, 'faceWidthX')
	depthY = retnumber(parent, 'faceDepthY')
	left = retnumber(parent, 'faceLeft')
	back = retnumber(parent, 'faceRear')
	top = retnumber(parent, 'faceTop')
	tool = retnumber(parent, 'faceTool')
	diam = retnumber(parent, 'faceToolDia')
	radius = diam / 2
	rpm = retnumber(parent, 'faceRPM')
	feed = retnumber(parent, 'faceFeed')
	if parent.faceStep.text() != '':
		stepPercent = retnumber(parent, 'faceStep') * 0.01
	else:
		stepPercent = 0.75
	safeZ = retnumber(parent, 'faceSafeZ')
	leadin = retnumber(parent, 'faceLeadIn')
	cutdepth = retnumber(parent, 'faceFullDepth')
	if parent.faceStepDepth.text() == '':
		stepdepth = cutdepth
	else:
		stepdepth = abs(retnumber(parent, 'faceStepDepth'))

	step = min(widthX, depthY)
	cutwidth = diam * stepPercent

	steps = int(round((min(widthX, depthY) + (2 * cutwidth)) / cutwidth, 0)/2)
	#print(steps)

	# setup initial path ends
	# end + radius - cutwidth = path
	plusX = (left + widthX) + radius - cutwidth
	minusX = left - radius + cutwidth
	plusY = back + radius - cutwidth
	minusY = (back - depthY) - radius + cutwidth

	parent.facePTE.clear()
	parent.facePTE.append(f';Face Stock X{left} to X{left + widthX} '
		f'Y{back} to Y{back - depthY}')
	parent.facePTE.append(f';Initial Path X{minusX - leadin} '
		f'Y{plusY} to X{plusX} to Y{minusY} to X{minusX} to Y{round(plusY - cutwidth, 4)}')
	parent.facePTE.append(f'{parent.unitsBG.checkedButton().property("units")}')
	parent.facePTE.append(f'{parent.preambleLE.text()}')

	parent.facePTE.append(f'G0 Z{safeZ}')

	if tool:
		parent.facePTE.append(f'T{int(tool)} M6 G43')
	parent.facePTE.append(f'M3 S{rpm} F{feed}')
	# raise top to make even number of full depth cuts if not even
	depthPasses = ceil(cutdepth / stepdepth)
	parent.facePTE.append(f';Steps {depthPasses}')
	top = round((depthPasses * stepdepth) - cutdepth, 4)
	parent.facePTE.append(f';Top {top}')
	currentZ = top

	# depth loop
	while currentZ > cutdepth:
		parent.facePTE.append(f'G0 Z{safeZ:.4f}')

		plusX = (left + widthX) + radius - cutwidth
		minusX = left - radius + cutwidth
		plusY = back + radius - cutwidth
		minusY = (back - depthY) - radius + cutwidth
		parent.facePTE.append(f'G0 X{minusX  - leadin:.4f} Y{plusY:.4f}')

		nextZ = currentZ - stepdepth
		parent.facePTE.append(f'G1 Z{nextZ:.4f}')
		currentZ = nextZ

		# path loop
		for i in range(steps):
			parent.facePTE.append(f'G1 X{plusX - cutwidth:.4f} Y{plusY:.4f}')
			plusY = plusY - cutwidth
			parent.facePTE.append(f'G2 X{plusX:.4f} Y{plusY:.4f} I0.0 J-{cutwidth:.4f}')
			parent.facePTE.append(f'G1 X{plusX:.4f} Y{minusY + cutwidth:.4f}')
			plusX = plusX - cutwidth
			parent.facePTE.append(f'G2 X{plusX:.4f} Y{minusY:.4f} I-{cutwidth:.4f} J0.0')
			parent.facePTE.append(f'G1 X{minusX + cutwidth:.4f} Y{minusY:.4f}')
			minusY = minusY + cutwidth
			w = plusX - minusX
			d = plusY - minusY
			if d <= 0.0 or w <= 0.0: break
			parent.facePTE.append(f'G2 X{minusX:.4f} Y{minusY:.4f} I0.0 J{cutwidth:.4f}')
			parent.facePTE.append(f'G1 X{minusX:.4f} Y{plusY - cutwidth:.4f}')
			minusX = minusX + cutwidth
			parent.facePTE.append(f'G2 X{minusX:.4f} Y{plusY:.4f} I{cutwidth:.4f} J0.0')
		parent.facePTE.append(f'G0 Z{safeZ:.4f}')
	if parent.faceReturnCB.isChecked():
		parent.facePTE.append(f'G0 X0 Y0')
	if parent.faceProgEndCB.isChecked():
		parent.facePTE.append('M2')

	# parent.facePTE.append(f'{}')

def copy(parent):
	qclip = QApplication.clipboard()
	qclip.setText(parent.facePTE.toPlainText())
	parent.statusbar.showMessage('G code copied to clipboard')

def send(parent):
	parent.gcodePTE.append(parent.facePTE.toPlainText())

def save(parent):
	options = QFileDialog.Options()
	options |= QFileDialog.DontUseNativeDialog
	ncDir = os.path.join(os.path.expanduser("~"), 'linuxcnc/nc_files')
	fileName, _ = QFileDialog.getSaveFileName(parent,
	caption="Save File", directory=ncDir,
	filter="All Files (*);;G Code Files (*.ngc)", options=options)
	if fileName:
		with open(fileName, 'w') as f:
			f.writelines(parent.facePTE.toPlainText())

def delete(parent):
	cursor = parent.facePTE.textCursor()
	cursor.select(QTextCursor.LineUnderCursor)
	cursor.removeSelectedText()
	cursor.deleteChar()

def selectLine(parent):
	fmt = QTextCharFormat()
	fmt.setUnderlineColor(Qt.red)
	fmt.setUnderlineStyle(QTextCharFormat.SingleUnderline)
	#fmt.setUnderlineStyle(QTextCharFormat.DashUnderline)
	#fmt.setUnderlineStyle(QTextCharFormat.DotLine)
	#fmt.setUnderlineStyle(QTextCharFormat.DashDotLine)
	#fmt.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
	#fmt.setUnderlineStyle(QTextCharFormat.WaveUnderline)
	cursor = parent.facePTE.textCursor()
	position = cursor.position()
	cursor.select(QTextCursor.Document)
	cursor.setCharFormat(QTextCharFormat())
	cursor.clearSelection()
	cursor.setPosition(position)
	cursor.select(QTextCursor.LineUnderCursor)
	cursor.setCharFormat(fmt)

def saveTemplate(parent):
	path = files.saveFilePath(parent,'face')
	face = ['[FACING]\n']
	face.append(f'X_WIDTH = {parent.faceWidthX.text().strip()}\n')
	face.append(f'Y_DEPTH = {parent.faceDepthY.text().strip()}\n')
	face.append(f'X_LEFT = {parent.faceLeft.text().strip()}\n')
	face.append(f'Y_REAR = {parent.faceRear.text().strip()}\n')
	face.append(f'TOOL = {parent.faceTool.text().strip()}\n')
	face.append(f'TOOL_DIA = {parent.faceToolDia.text().strip()}\n')
	face.append(f'RPM = {parent.faceRPM.text().strip()}\n')
	face.append(f'FEED = {parent.faceFeed.text().strip()}\n')
	face.append(f'STEP = {parent.faceStep.text().strip()}\n')
	face.append(f'SAFE_Z = {parent.faceSafeZ.text().strip()}\n')
	face.append(f'LEAD_IN = {parent.faceLeadIn.text().strip()}\n')
	face.append(f'Z_DEPTH = {parent.faceFullDepth.text().strip()}\n')
	face.append(f'Z_STEP = {parent.faceStepDepth.text().strip()}\n')
	face.append(f'RETURN = {parent.faceReturnCB.isChecked()}\n')
	face.append(f'PROG_END = {parent.faceProgEndCB.isChecked()}\n')

	with open(path, 'w') as f:
		f.writelines(face) 


def openTemplate(parent):
	path = files.openFile(parent,'face')
	template = [
	['FACING', 'X_WIDTH', 'faceWidthX'],
	['FACING', 'Y_DEPTH', 'faceDepthY'],
	['FACING', 'X_LEFT', 'faceLeft'],
	['FACING', 'Y_REAR', 'faceRear'],
	['FACING', 'TOOL', 'faceTool'],
	['FACING', 'TOOL_DIA', 'faceToolDia'],
	['FACING', 'RPM', 'faceRPM'],
	['FACING', 'FEED', 'faceFeed'],
	['FACING', 'STEP', 'faceStep'],
	['FACING', 'SAFE_Z', 'faceSafeZ'],
	['FACING', 'LEAD_IN', 'faceLeadIn'],
	['FACING', 'Z_DEPTH', 'faceFullDepth'],
	['FACING', 'Z_STEP', 'faceStepDepth'],
	['FACING', 'RETURN', 'faceReturnCB'],
	['FACING', 'PROG_END', 'faceProgEndCB'],
	]

	config = configparser.ConfigParser(strict=False)
	config.optionxform = str
	config.read(path)

	for item in template:
		if config.has_option(item[0], item[1]):
			if isinstance(getattr(parent, item[2]), QLabel):
				getattr(parent, item[2]).setText(config[item[0]][item[1]])
			if isinstance(getattr(parent, item[2]), QLineEdit):
				getattr(parent, item[2]).setText(config[item[0]][item[1]])
			if isinstance(getattr(parent, item[2]), QSpinBox):
				getattr(parent, item[2]).setValue(abs(int(config[item[0]][item[1]])))
			if isinstance(getattr(parent, item[2]), QDoubleSpinBox):
				getattr(parent, item[2]).setValue(float(config[item[0]][item[1]]))
			if isinstance(getattr(parent, item[2]), QCheckBox):
				getattr(parent, item[2]).setChecked(eval(config[item[0]][item[1]]))
			if isinstance(getattr(parent, item[2]), QGroupBox):
				getattr(parent, item[2]).setChecked(eval(config[item[0]][item[1]]))
				#print(self.config[item[0]][item[1]])
			if isinstance(getattr(parent, item[2]), QComboBox):
				index = getattr(v, item[2]).findData(config[item[0]][item[1]])
				if index >= 0:
					getattr(parent, item[2]).setCurrentIndex(index)


