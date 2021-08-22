gcodes = {
	'G81':['cannedRetractLE', 'repeteLE'],
	'G82':['cannedRetractLE', 'repeteLE', 'dwellLE'],
	'G83':['cannedRetractLE', 'repeteLE', 'peckLE'],
	'G84':['cannedRetractLE', 'repeteLE', 'dwellLE', 'spindleSB'],
	'G85':['cannedRetractLE', 'repeteLE'],
	'G86':['cannedRetractLE', 'repeteLE', 'dwellLE', 'spindleSB'],
	'G89':['cannedRetractLE', 'repeteLE', 'dwellLE']
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
	parent.cannedZcoordLE.setFocus()

def zcoord(parent):
	x = parent.cannedXcoordLE.text()
	y = parent.cannedYcoordLE.text()
	z = parent.cannedZcoordLE.text()
	parent.cannedCoordPTE.appendPlainText(f'X{x} Y{y} Z{z}')
	parent.cannedXcoordLE.setFocus()
	parent.cannedXcoordLE.clear()
	parent.cannedYcoordLE.clear()
	parent.cannedZcoordLE.clear()

def gcode(parent):
	parent.cannedGcodePTE.clear()
	cycle = parent.cannedCycleBG.checkedButton().text()
	#print(cycles[cycle](parent))
	coords = parent.cannedCoordPTE.toPlainText().split('\n')
	#print(len(coords))
	parent.cannedGcodePTE.appendPlainText(f'; {cycle} Cycle')
	startZ = parent.cannedZstartLE.text()
	parent.cannedGcodePTE.appendPlainText(f'G0 Z{startZ}')
	startX = parent.cannedXstartLE.text()
	startY =  parent.cannedYstartLE.text()
	parent.cannedGcodePTE.appendPlainText(f'X{startX} Y{startY}')
	if parent.cannedToolLE.text() != '':
		tool = parent.cannedToolLE.text()
		parent.cannedGcodePTE.appendPlainText(f'T{tool} M6')
	retract = parent.cannedRetractBG.checkedButton().text()
	distance = parent.cannedDistanceBG.checkedButton().text()
	parent.cannedGcodePTE.appendPlainText(f'{retract} {distance}')

	cycleline = []
	cycleline.append(cycle + ' ')
	cycleline.append(coords[0] + ' ')
	for item in gcodes[cycle]:
		word = getattr(parent, item).property('word')
		value = getattr(parent, item).text()
		if len(value) > 0:
			cycleline.append(f'{word} {value}')
	#print(cycleline)
	firstline = ''.join(cycleline)
	parent.cannedGcodePTE.appendPlainText(f'{firstline}')

	parent.cannedGcodePTE.appendPlainText('M2')
	# parent.cannedGcodePTE.appendPlainText(f'{}')


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
