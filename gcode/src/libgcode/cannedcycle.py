from PyQt5.QtWidgets import QApplication

gcodes = {
	'G81':['canRetractLE', 'repeteLE'],
	'G82':['canRetractLE', 'repeteLE', 'dwellLE'],
	'G83':['canRetractLE', 'repeteLE', 'peckLE'],
	'G84':['canRetractLE', 'repeteLE', 'dwellLE', 'spindleSB'],
	'G85':['canRetractLE', 'repeteLE'],
	'G86':['canRetractLE', 'repeteLE', 'dwellLE', 'spindleSB'],
	'G89':['canRetractLE', 'repeteLE', 'dwellLE']
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
	words = ['dwellLE', 'spindleSB', 'peckLE']
	for item in words:
		getattr(parent, item).setEnabled(False)
	cycle = parent.cannedCycleBG.checkedButton().text()
	for item in gcodes[cycle]:
		getattr(parent, item).setEnabled(True)
	parent.cannedGeneratePB.setEnabled(True)

def xcoord(parent):
	parent.cannedYcoordLE.setFocus()

def ycoord(parent):
	x = parent.canCoordPTE.text()
	y = parent.cannedYcoordLE.text()
	parent.cannedCoordPTE.appendPlainText(f'X{x} Y{y}')
	parent.canCoordPTE.setFocus()
	parent.canCoordPTE.clear()
	parent.cannedYcoordLE.clear()


def gcode(parent):
	parent.canGcodePTE.clear()
	cycle = parent.cannedCycleBG.checkedButton().text()
	#print(cycles[cycle](parent))
	coords = parent.canCoordPTE.toPlainText().split('\n')
	#print(len(coords))
	parent.canGcodePTE.appendPlainText(f'; {cycle} Cycle')
	rpm = parent.canRpmLE.text()
	feed = parent.canFeedLE.text()
	parent.canGcodePTE.appendPlainText(f'S{rpm} F{feed}')
	if parent.canToolLE.text() != '':
		tool = parent.canToolLE.text()
		parent.canGcodePTE.appendPlainText(f'T{tool} M6')
	startZ = parent.cannedZstartLE.text()
	parent.canGcodePTE.appendPlainText(f'G0 Z{startZ}')
	startX = parent.cannedXstartLE.text()
	startY =  parent.cannedYstartLE.text()
	parent.canGcodePTE.appendPlainText(f'X{startX} Y{startY}')
	retract = parent.cannedRetractBG.checkedButton().text()
	distance = parent.cannedDistanceBG.checkedButton().text()
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

	parent.canGcodePTE.appendPlainText('M80')
	parent.canGcodePTE.appendPlainText('M5')
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
		parent.cannedRpmLE.setText(items[2])
		parent.cannedFeedLE.setText(items[4])
	#print(items[2])
	#print(items[4])
