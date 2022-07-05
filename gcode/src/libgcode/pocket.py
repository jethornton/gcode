import os, configparser
from math import ceil
from PyQt5.QtWidgets import (QLineEdit, QSpinBox, QCheckBox, QComboBox,
	QLabel, QGroupBox, QDoubleSpinBox, QFileDialog, QMessageBox, QFileDialog)

from PyQt5.QtGui import QTextCursor, QTextCharFormat, QTextCharFormat
from PyQt5.QtCore import Qt

from libgcode import files

def retnumber(parent, i): # get line edit name then test for number
	if getattr(parent, i).text():
		try:
			num = float(getattr(parent, i).text())
			return num
		except Exception as e:
			print(e)
			name = getattr(parent, i).property("name")
			text = getattr(parent, i).text()
			print(i)
			parent.errorMsgOk(f'{name} {text} is not a number', 'Error')
			return False

def generate(parent):
	widthX = retnumber(parent, 'pocketWidthX')
	depthY = retnumber(parent, 'pocketDepthY')
	left = retnumber(parent, 'pocketLeft')
	back = retnumber(parent, 'pocketRear')
	top = retnumber(parent, 'pocketTop')
	corner = retnumber(parent, 'pocketRadius')
	tool = retnumber(parent, 'pocketTool')
	diam = retnumber(parent, 'pocketToolDia')
	rpm = retnumber(parent, 'pocketRPM')
	feed = retnumber(parent, 'pocketFeed')
	stepPercent = retnumber(parent, 'pocketStep') * 0.01
	safeZ = retnumber(parent, 'pocketSafeZ')
	leadin = retnumber(parent, 'pocketLeadIn')
	depthZ = retnumber(parent, 'pocketCutDepth')
	doc = abs(retnumber(parent, 'pocketStepDepth'))
	woc = diam * stepPercent
	steps = ceil((min(widthX, depthY) / 2) / woc)
	plusX = (left + widthX) - woc
	minusX = left + woc
	plusY = back - woc
	minusY = (back - depthY) + woc

	parent.pocketPTE.clear()

	parent.pocketPTE.append(f';Pocket Size X{left} to X{left + widthX} '
		f'Y{back} to Y{back - depthY}')

	parent.pocketPTE.append(f'{parent.unitsBG.checkedButton().property("units")}')
	parent.pocketPTE.append(f'{parent.preambleLE.text()}')

	if tool:
		parent.pocketPTE.append(f'T{int(tool)} M6 G43')
	parent.pocketPTE.append(f'M3 S{rpm} F{feed}')
	# raise top to make even number of full depth cuts if not even
	depthPasses = ceil(abs(depthZ) / doc)
	parent.pocketPTE.append(f';Steps {depthPasses}')
	top = (depthPasses * doc) - abs(depthZ)
	parent.pocketPTE.append(f';Top {top:.4f}')
	parent.pocketPTE.append(f'G0 Z{safeZ:.4f}')
	currentZ = top
	passes = int(ceil((depthY - diam) / woc)/2)

	if passes % 2 != 0:
		passes = passes + 1
	# if passes is odd then add one pass and make the first pass 1/2 width
	print(f'passes {passes}')

	if widthX >= depthY:
		material = (depthY - diam) / 2
		if material % woc > 0:
			woc = material % woc

		minusX = left + (passes * woc)
		plusX = (left + widthX) - passes * woc
		minusY = back - (depthY / 2)
		plusY = minusY
	else:
		print(f'cutwidth {woc}')

	# depth loop
	print(f'currentZ {currentZ} depthZ {depthZ}')
	nextZ = currentZ
	while currentZ > depthZ:
		radius = woc
		currentZ = nextZ
		parent.pocketPTE.append(f'G0 Z{safeZ:.4f}')

		minusX = left + (passes * woc)
		plusX = (left + widthX) - passes * woc
		minusY = back - (depthY / 2)
		plusY = minusY

		parent.pocketPTE.append(f'G0 X{minusX:.4f} Y{plusY:.4f}')
		parent.pocketPTE.append(f'G1 Z{currentZ:.4f}')
		parent.pocketPTE.append(f'G0 X{minusX:.4f} Y{minusY:.4f}')
		parent.pocketPTE.append(f'G1 Z{currentZ:.4f}')
		currentZ = currentZ - doc
		parent.pocketPTE.append(f'G1 X{plusX:.4f} Y{minusY:.4f} Z{currentZ:.4f}')
		minusX = minusX - woc
		parent.pocketPTE.append(f'G1 X{minusX:.4f} Y{plusY:.4f}')

		for i in range(1, passes):
			parent.pocketPTE.append(f'; pass {i}')
			minusY = minusY - woc
			remainingY = abs((back - depthY) - minusY)
			if remainingY < corner:
				radius = corner - remainingY
			parent.pocketPTE.append(f'G1 X{minusX:.4f} Y{minusY + radius:.4f}')
			parent.pocketPTE.append(f'G3 X{minusX + radius:.4f} Y{minusY:.4f} I{radius:.4f} J0.0')
			plusX = plusX + woc
			parent.pocketPTE.append(f'G1 X{plusX - radius:.4f} Y{minusY:.4f}')
			parent.pocketPTE.append(f'G3 X{plusX:.4f} Y{minusY + radius:.4f} I0.0 J{radius:.4f}')
			plusY = plusY + woc
			parent.pocketPTE.append(f'G1 X{plusX:.4f} Y{plusY - radius:.4f}')
			parent.pocketPTE.append(f'G3 X{plusX - radius:.4f} Y{plusY:.4f} I-{radius:.4f} J0.0')
			if minusX - woc > left:
				minusX = minusX - woc
			parent.pocketPTE.append(f'G1 X{minusX + radius:.4f} Y{plusY:.4f}')
			parent.pocketPTE.append(f'G3 X{minusX:.4f} Y{plusY - radius:.4f} I0.0 J-{radius:.4f}')

		parent.pocketPTE.append(f'G0 Z{safeZ:.4f}')
		nextZ = currentZ - doc

	if parent.devel:
		pocket(parent)
	if parent.pocketProgEndCB.isChecked():
		parent.pocketPTE.append('M2')

	# draw the pocket pocketReturnCB
def pocket(parent):
	widthX = retnumber(parent, 'pocketWidthX')
	depthY = retnumber(parent, 'pocketDepthY')
	left = retnumber(parent, 'pocketLeft')
	back = retnumber(parent, 'pocketRear')
	top = retnumber(parent, 'pocketTop')
	corner = retnumber(parent, 'pocketRadius')
	feed = retnumber(parent, 'pocketFeed')
	rpm = retnumber(parent, 'pocketRPM')
	plusX = (left + widthX)
	minusX = left
	plusY = back
	minusY = (back - depthY)

	parent.pocketPTE.append(f'{parent.unitsBG.checkedButton().property("units")}')
	parent.pocketPTE.append(f'{parent.preambleLE.text()}')
	parent.pocketPTE.append(f'M3 S{rpm} F{feed}')
	parent.pocketPTE.append('; Drawing the pocket')
	parent.pocketPTE.append(f'G0 X{minusX + corner} Y{plusY} Z0')
	parent.pocketPTE.append(f'G1 X{plusX - corner} Y{plusY}')
	parent.pocketPTE.append(f'G2 X{plusX} Y{plusY - corner} I0.0 J-{corner}')
	parent.pocketPTE.append(f'G1 X{plusX} Y{minusY + corner}')
	parent.pocketPTE.append(f'G2 X{plusX - corner} Y{minusY} I-{corner} J0.0')
	parent.pocketPTE.append(f'G1 X{minusX + corner} Y{minusY}')
	parent.pocketPTE.append(f'G2 X{minusX} Y{minusY + corner} I0.0 J{corner}')
	parent.pocketPTE.append(f'G1 X{minusX} Y{plusY - corner}')
	parent.pocketPTE.append(f'G2 X{minusX + corner} Y{plusY} I{corner} J0.0')

def copy(parent):
	qclip = QApplication.clipboard()
	qclip.setText(parent.pocketPTE.toPlainText())
	parent.statusbar.showMessage('G code copied to clipboard')

def send(parent):
	parent.gcodePTE.append(parent.pocketPTE.toPlainText())


def save(parent):
	if parent.devel:
		with open('/home/john/linuxcnc/nc_files/pocket.ngc', 'w') as f:
			f.writelines(parent.pocketPTE.toPlainText())
	else:
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		ncDir = os.path.join(os.path.expanduser("~"), 'linuxcnc/nc_files')
		fileName, _ = QFileDialog.getSaveFileName(parent,
		caption="Save File", directory=ncDir,
		filter="All Files (*);;G Code Files (*.ngc)", options=options)
		if fileName:
			with open(fileName, 'w') as f:
				f.writelines(parent.pocketPTE.toPlainText())

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
	cursor = parent.pocketPTE.textCursor()
	position = cursor.position()
	cursor.select(QTextCursor.Document)
	cursor.setCharFormat(QTextCharFormat())
	cursor.clearSelection()
	cursor.setPosition(position)
	cursor.select(QTextCursor.LineUnderCursor)
	cursor.setCharFormat(fmt)

def saveTemplate(parent):
	path = files.saveFilePath(parent,'pocket')
	face = ['[POCKET]\n']
	face.append(f'X_WIDTH = {parent.pocketWidthX.text().strip()}\n')
	face.append(f'Y_DEPTH = {parent.pocketDepthY.text().strip()}\n')
	face.append(f'X_LEFT = {parent.pocketLeft.text().strip()}\n')
	face.append(f'Y_REAR = {parent.pocketRear.text().strip()}\n')
	face.append(f'TOOL = {parent.pocketTool.text().strip()}\n')
	face.append(f'TOOL_DIA = {parent.pocketToolDia.text().strip()}\n')
	face.append(f'RPM = {parent.pocketRPM.text().strip()}\n')
	face.append(f'FEED = {parent.pocketFeed.text().strip()}\n')
	face.append(f'STEP = {parent.pocketStep.text().strip()}\n')
	face.append(f'SAFE_Z = {parent.pocketSafeZ.text().strip()}\n')
	face.append(f'LEAD_IN = {parent.pocketLeadIn.text().strip()}\n')
	face.append(f'Z_DEPTH = {parent.pocketCutDepth.text().strip()}\n')
	face.append(f'Z_STEP = {parent.pocketStepDepth.text().strip()}\n')
	face.append(f'RETURN = {parent.pocketReturnCB.isChecked()}\n')
	face.append(f'PROG_END = {parent.pocketProgEndCB.isChecked()}\n')

	with open(path, 'w') as f:
		f.writelines(face) 


def openTemplate(parent):
	path = files.openFile(parent,'pocket')
	template = [
	['POCKET', 'X_WIDTH', 'pocketWidthX'],
	['POCKET', 'Y_DEPTH', 'pocketDepthY'],
	['POCKET', 'X_LEFT', 'pocketLeft'],
	['POCKET', 'Y_REAR', 'pocketRear'],
	['POCKET', 'TOOL', 'pocketTool'],
	['POCKET', 'TOOL_DIA', 'pocketToolDia'],
	['POCKET', 'RPM', 'pocketRPM'],
	['POCKET', 'FEED', 'pocketFeed'],
	['POCKET', 'STEP', 'pocketStep'],
	['POCKET', 'SAFE_Z', 'pocketSafeZ'],
	['POCKET', 'LEAD_IN', 'pocketLeadIn'],
	['POCKET', 'Z_DEPTH', 'pocketCutDepth'],
	['POCKET', 'Z_STEP', 'pocketStepDepth'],
	['POCKET', 'RETURN', 'pocketReturnCB'],
	['POCKET', 'PROG_END', 'pocketProgEndCB'],
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


