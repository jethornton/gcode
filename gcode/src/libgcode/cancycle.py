from PyQt5.QtWidgets import QApplication

gcodes = {
	'G81':['canRetractLE', 'canRepeteLE'],
	'G82':['canRetractLE', 'canRepeteLE', 'canDwellLE'],
	'G83':['canRetractLE', 'canRepeteLE', 'canPeckLE'],
	'G84':['canRetractLE', 'canRepeteLE', 'canDwellLE', 'canSpindleSB'],
	'G85':['canRetractLE', 'canRepeteLE'],
	'G86':['canRetractLE', 'canRepeteLE', 'canDwellLE', 'canSpindleSB'],
	'G89':['canRetractLE', 'canRepeteLE', 'canDwellLE']
	}

required = {
	'G81':['canRetractLE'],
	'G82':['canRetractLE', 'canDwellLE'],
	'G83':['canRetractLE', 'canPeckLE'],
	'G84':['canRetractLE', 'canDwellLE', 'canSpindleSB'],
	'G85':['canRetractLE'],
	'G86':['canRetractLE', 'canDwellLE', 'canSpindleSB'],
	'G89':['canRetractLE', 'canDwellLE']
	}

def g81(parent):
	return('G81 X Y Z R L')

def g82(parent):
	return('G82 X Y Z R L P')

def g83(parent):
	return('G83 X Y Z R L Q')

def g84(parent):
	return('G84 X Y Z R L P $')

def g85(parent):
	return('G85 X Y Z R L')

def g86(parent):
	return('G86 X Y Z R L P $')

def g89(parent):
	return('G89 X Y Z R L P')



cycles = {
	'G81':g81,
	'G82':g82,
	'G83':g83,
	'G84':g84,
	'G85':g85,
	'G86':g86,
	'G89':g89
	}

def update(parent):
	words = ['canDwellLE', 'canSpindleSB', 'canPeckLE']
	for item in words:
		getattr(parent, item).setEnabled(False)
	cycle = parent.canCycleBG.checkedButton().text()
	for item in gcodes[cycle]:
		getattr(parent, item).setEnabled(True)
	parent.canGeneratePB.setEnabled(True)

def xcoord(parent):
	parent.canYcoordLE.setFocus()

def ycoord(parent):
	x = parent.canXcoordLE.text()
	y = parent.canYcoordLE.text()
	parent.canCoordPTE.appendPlainText(f'X{x} Y{y}')
	parent.canXcoordLE.setFocus()
	parent.canXcoordLE.clear()
	parent.canYcoordLE.clear()


def gcode(parent):
	if parent.canGenerateBG.checkedButton().text() == 'Replace':
		parent.canGcodePTE.clear()
	cycle = parent.canCycleBG.checkedButton().text()
	coords = parent.canCoordPTE.toPlainText().split('\n')

	#print(required[cycle])
	for item in required[cycle]:
		if getattr(parent, item).text() == '':
			name = getattr(parent, item).property('name')
			parent.canGcodePTE.appendPlainText(f'{name} Must Not be Blank')
			return
	if parent.canRepeteLE.text() != '':
		error = False
		#print(coords)
		#print(parent.canRepeteLE.text())
		#print(parent.canDistanceBG.checkedButton().text())
		if int(parent.canRepeteLE.text()) < 2:
			parent.canGcodePTE.appendPlainText('Repeat must be 2 or more for the L word')
			error = True
		if parent.canDistanceBG.checkedButton().text() == 'G90':
			parent.canGcodePTE.appendPlainText('G91 must be selected for the L word')
			error = True
		if len(coords) > 1:
			parent.canGcodePTE.appendPlainText('Only One hole position is used for the L word')
			error = True
		if error:
			return

	#print(cycles[cycle](parent))
	#print(len(coords))
	parent.canGcodePTE.appendPlainText(f'; {cycle} Cycle')
	rpm = parent.canRpmLE.text()
	feed = parent.canFeedLE.text()
	parent.canGcodePTE.appendPlainText(f'S{rpm} F{feed}')
	if parent.canToolLE.text() != '':
		tool = parent.canToolLE.text()
		parent.canGcodePTE.appendPlainText(f'T{tool} M6')
	startZ = parent.canZstartLE.text()
	parent.canGcodePTE.appendPlainText(f'G0 Z{startZ}')
	startX = parent.canXstartLE.text()
	startY =  parent.canYstartLE.text()
	parent.canGcodePTE.appendPlainText(f'X{startX} Y{startY}')
	retract = parent.canRetractBG.checkedButton().text()
	distance = parent.canDistanceBG.checkedButton().text()
	parent.canGcodePTE.appendPlainText(f'{retract} {distance}')
	parent.canGcodePTE.appendPlainText('M3')
	cycleline = []
	cycleline.append(f'{cycle} ')
	cycleline.append(f'{coords[0]} ')
	cycleline.append(f'Z{parent.canZdepthLE.text()} ')
	for item in gcodes[cycle]:
		word = getattr(parent, item).property('word')
		value = getattr(parent, item).text()
		if len(value) > 0:
			cycleline.append(f'{word}{value} ')
	#print(cycleline)
	firstline = ''.join(cycleline)
	parent.canGcodePTE.appendPlainText(f'{firstline}')
	if len(coords) > 1:
		for item in coords[1:]:
			parent.canGcodePTE.appendPlainText(f'{item}')

	parent.canGcodePTE.appendPlainText('G80')
	parent.canGcodePTE.appendPlainText('M5')
	if parent.canEndReturnCB.isChecked():
		parent.canGcodePTE.appendPlainText('G0 Z0')
		parent.canGcodePTE.appendPlainText('G0 X0 Y0')
	if parent.canProgEndCB.isChecked():
		parent.canGcodePTE.appendPlainText('M2')
	# parent.canGcodePTE.appendPlainText(f'{}')

def copy(parent):
	qclip = QApplication.clipboard()
	qclip.setText(parent.canGcodePTE.toPlainText())
	parent.statusbar.showMessage('G code copied to clipboard')

def drill(parent):
	cursor = parent.drillPTE.textCursor()
	info = cursor.selectedText().split()
	parent.drillRpmLE.setText(info[2])
	parent.drillFeedLE.setText(info[4])

def get(parent):
	cursor = parent.drillPTE.textCursor()
	items = cursor.selectedText().split()
	if len(items) > 4:
		#print(len(items))
		parent.canRpmLE.setText(items[2])
		parent.canFeedLE.setText(items[4])
	#print(items[2])
	#print(items[4])
