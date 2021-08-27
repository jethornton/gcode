import os
from math import ceil
from PyQt5.QtWidgets import QMessageBox, QApplication, QFileDialog
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QTextCharFormat
from PyQt5.QtCore import Qt

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
			return num
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
			parent.facePTE.appendPlainText(f'{name} is required')
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
	stepPercent = retnumber(parent, 'faceStep') * 0.01
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
	parent.facePTE.appendPlainText(f';Face Stock X{left} to X{left + widthX} '
		f'Y{back} to Y{back - depthY}')
	parent.facePTE.appendPlainText(f';Inital Path X{minusX - leadin} '
		f'Y{plusY} to X{plusX} to Y{minusY} to X{minusX} to Y{plusY - cutwidth}')
	parent.facePTE.appendPlainText(f'{parent.unitsBG.checkedButton().property("units")}')
	parent.facePTE.appendPlainText(f'{parent.preambleLE.text()}')

	parent.facePTE.appendPlainText(f'G0 Z{safeZ}')

	if tool:
		parent.facePTE.appendPlainText(f'T{int(tool)} M6 G43')
	parent.facePTE.appendPlainText(f'M3 S{rpm} F{feed}')
	# raise top to make even number of full depth cuts if not even
	depthPasses = ceil(cutdepth / stepdepth)
	parent.facePTE.appendPlainText(f';Steps {depthPasses}')
	top = round((depthPasses * stepdepth) - cutdepth, 4)
	parent.facePTE.appendPlainText(f';Top {top}')
	currentZ = top

	# depth loop
	while currentZ > cutdepth:
		parent.facePTE.appendPlainText(f'G0 Z{safeZ:.4f}')

		plusX = (left + widthX) + radius - cutwidth
		minusX = left - radius + cutwidth
		plusY = back + radius - cutwidth
		minusY = (back - depthY) - radius + cutwidth
		parent.facePTE.appendPlainText(f'G0 X{minusX  - leadin:.4f} Y{plusY:.4f}')

		nextZ = currentZ - stepdepth
		parent.facePTE.appendPlainText(f'G1 Z{nextZ:.4f}')
		currentZ = nextZ

		# path loop
		for i in range(steps):
			parent.facePTE.appendPlainText(f'G1 X{plusX - cutwidth:.4f} Y{plusY:.4f}')
			plusY = plusY - cutwidth
			parent.facePTE.appendPlainText(f'G2 X{plusX:.4f} Y{plusY:.4f} I0.0 J-{cutwidth:.4f}')
			parent.facePTE.appendPlainText(f'G1 X{plusX:.4f} Y{minusY + cutwidth:.4f}')
			plusX = plusX - cutwidth
			parent.facePTE.appendPlainText(f'G2 X{plusX:.4f} Y{minusY:.4f} I-{cutwidth:.4f} J0.0')
			parent.facePTE.appendPlainText(f'G1 X{minusX + cutwidth:.4f} Y{minusY:.4f}')
			minusY = minusY + cutwidth
			w = plusX - minusX
			d = plusY - minusY
			if d <= 0.0 or w <= 0.0: break
			parent.facePTE.appendPlainText(f'G2 X{minusX:.4f} Y{minusY:.4f} I0.0 J{cutwidth:.4f}')
			parent.facePTE.appendPlainText(f'G1 X{minusX:.4f} Y{plusY - cutwidth:.4f}')
			minusX = minusX + cutwidth
			parent.facePTE.appendPlainText(f'G2 X{minusX:.4f} Y{plusY:.4f} I{cutwidth:.4f} J0.0')
		parent.facePTE.appendPlainText(f'G0 Z{safeZ:.4f}')
	if parent.faceReturnCB.isChecked():
		parent.facePTE.appendPlainText(f'G0 X0 Y0')
	if parent.faceProgEndCB.isChecked():
		parent.facePTE.appendPlainText('M2')

	# parent.facePTE.appendPlainText(f'{}')

def copy(parent):
	qclip = QApplication.clipboard()
	qclip.setText(parent.facePTE.toPlainText())
	parent.statusbar.showMessage('G code copied to clipboard')

def send(parent):
	parent.gcodePTE.appendPlainText(parent.facePTE.toPlainText())

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
	#print('here')
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
