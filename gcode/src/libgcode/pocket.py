import os
from math import ceil
from PyQt5.QtWidgets import QMessageBox, QApplication, QFileDialog

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
	"""
	It is recommended that you program a tool path that keeps the milling cutter
	in full contact, rather than performing several parallel passes. When changing
	direction, include a small radial tool path to keep the cutter moving and
	constantly engaged

	start X pocket left - leadin
	cutter diamter / 2 is center 
	1" cutter 0.5" center -0.25" path is for 25%
	stepover cutter diameter * percent
	start Y = pocket rear minus cutter radius + step
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
	widthX = retnumber(parent, 'pocketWidthX')
	depthY = retnumber(parent, 'pocketDepthY')
	left = retnumber(parent, 'pocketLeft')
	back = retnumber(parent, 'pocketRear')
	top = retnumber(parent, 'pocketTop')
	tool = retnumber(parent, 'pocketTool')
	diam = retnumber(parent, 'pocketToolDia')
	radius = diam / 2
	rpm = retnumber(parent, 'pocketRPM')
	feed = retnumber(parent, 'pocketFeed')
	stepPercent = retnumber(parent, 'pocketStep') * 0.01
	safeZ = retnumber(parent, 'pocketSafeZ')
	leadin = retnumber(parent, 'pocketLeadIn')
	cutdepth = retnumber(parent, 'pocketCutDepth')
	#print(cutdepth)
	stepdepth = retnumber(parent, 'pocketStepDepth')

	step = min(widthX, depthY)
	cutwidth = diam * stepPercent

	steps = int(round((min(widthX, depthY) + (2 * cutwidth)) / cutwidth, 0)/2)
	#print(steps)

	# setup initial path ends
	# end + radius - cutwidth = path
	plusX = (left + widthX) - radius
	minusX = left + radius
	plusY = back - radius
	minusY = (back - depthY) + radius

	parent.pocketPTE.clear()
	parent.pocketPTE.appendPlainText(f';Pocket Size X{left} to X{left + widthX} '
		f'Y{back} to Y{back - depthY}')
	parent.pocketPTE.appendPlainText(f';Inital Path X{minusX} '
		f'Y{plusY} to X{plusX} to Y{minusY} to X{minusX} to Y{plusY}')
	parent.facePTE.appendPlainText(f'{parent.unitsBG.checkedButton().property("units")}')
	parent.pocketPTE.appendPlainText(f'G0 Z{safeZ}')

	if tool:
		parent.pocketPTE.appendPlainText(f'T{int(tool)} M6 G43')
	parent.pocketPTE.appendPlainText(f'G0 X{minusX  - leadin} Y{plusY}')
	parent.pocketPTE.appendPlainText(f'M3 S{rpm} F{feed}')
	# raise top to make even number of full depth cuts if not even
	depthPasses = ceil(cutdepth / stepdepth)
	parent.pocketPTE.appendPlainText(f';Steps {depthPasses}')
	top = round((depthPasses * stepdepth) - cutdepth, 4)
	parent.pocketPTE.appendPlainText(f';Top {top}')
	return
	currentZ = top

	# depth loop
	while currentZ > cutdepth:
		parent.pocketPTE.appendPlainText(f'G0 Z{safeZ}')

		plusX = (left + widthX) + radius - cutwidth
		minusX = left - radius + cutwidth
		plusY = back + radius - cutwidth
		minusY = (back - depthY) - radius + cutwidth
		parent.pocketPTE.appendPlainText(f'G0 X{minusX  - leadin} Y{plusY}')

		nextZ = currentZ - stepdepth
		parent.pocketPTE.appendPlainText(f'G1 Z{nextZ}')
		currentZ = nextZ

		# path loop
		for i in range(steps):
			parent.pocketPTE.appendPlainText(f'G1 X{plusX - cutwidth} Y{plusY}')
			plusY = plusY - cutwidth
			parent.pocketPTE.appendPlainText(f'G2 X{plusX} Y{plusY} I0.0 J-{cutwidth}')
			parent.pocketPTE.appendPlainText(f'G1 X{plusX} Y{minusY + cutwidth}')
			plusX = plusX - cutwidth
			parent.pocketPTE.appendPlainText(f'G2 X{plusX} Y{minusY} I-{cutwidth} J0.0')
			parent.pocketPTE.appendPlainText(f'G1 X{minusX + cutwidth} Y{minusY}')
			minusY = minusY + cutwidth
			w = plusX - minusX
			d = plusY - minusY
			if d <= 0.0 or w <= 0.0: break
			parent.pocketPTE.appendPlainText(f'G2 X{minusX} Y{minusY} I0.0 J{cutwidth}')
			parent.pocketPTE.appendPlainText(f'G1 X{minusX} Y{plusY - cutwidth}')
			minusX = minusX + cutwidth
			parent.pocketPTE.appendPlainText(f'G2 X{minusX} Y{plusY} I{cutwidth} J0.0')
		parent.pocketPTE.appendPlainText(f'G0 Z{safeZ}')
	parent.pocketPTE.appendPlainText('M2')

	# parent.pocketPTE.appendPlainText(f'{}')

def copy(parent):
	qclip = QApplication.clipboard()
	qclip.setText(parent.pocketPTE.toPlainText())
	parent.statusbar.showMessage('G code copied to clipboard')

def save(parent):
	options = QFileDialog.Options()
	options |= QFileDialog.DontUseNativeDialog
	ncDir = os.path.join(os.path.expanduser("~"), 'linuxcnc/nc_files')
	fileName, _ = QFileDialog.getSaveFileName(parent,
	caption="Save File", directory=ncDir,
	filter="All Files (*);;G Code Files (*.ngc)", options=options)
	if fileName:
		with open(fileName, 'w') as f:
			f.writelines(parent.pocketPTE.toPlainText())
