from PyQt5.QtGui import QTextCursor, QTextCharFormat, QTextCharFormat
from PyQt5.QtCore import Qt

tapDrills = [
['#4-40 NC  ', '#43', 0.0890],
['#4-48 NF  ', '#42', 0.0935],
['#5-40 NC  ', '#38', 0.1015],
['#5-44 NF  ', '#37', 0.1040],
['#6-32 NC  ', '#36', 0.1065],
['#6-40 NF  ', '#33', 0.1130],
['#8-32 NC  ', '#29', 0.1360],
['#8-36 NF  ', '#29', 0.1360],
['#10-24 NC ', '#25', 0.1495],
['#10-32 NF ', '#21', 0.1590],
['1/4-20 NC ', '#7', 0.2010],
['1/4-28 NF ', '#3', 0.2130],
['5/16-18 NC', 'F', 0.2570],
['5/16-24 NF', 'I', 0.2720],
['3/8-16 NC ', '5/16"', 0.3125],
['3/8-24 NF ', 'Q', 0.3320],
['7/16-14 NC', 'U', 0.3680],
['7/16-20 NF', '25/64"', 0.3905],
['1/2-13 NC ', '27/64"', 0.4219],
['1/2-20 NF ', '29/64"', 0.4531],
['9/16-12 NC', '31/64"', 0.4844],
['9/16-18 NF', '33/64"', 0.5156],
['5/8-11 NC ', '17/32"', 0.5312],
['5/8-18 NF ', '37/64"', 0.5781],
['3/4-10 NC ', '21/32"', 0.6562],
]

def update(parent):
	if parent.drillMaterialBG.checkedButton() is None:
		return
	units = parent.drillUnitsBG.checkedButton().text()
	material = parent.drillMaterialBG.checkedButton().text()
	parent.drillSfmLb.setText(str(parent.drillSfmSB.value()))
	parent.drilliprLb.setText(str(parent.drilliprSB.value() * 0.001))

	# drillSfmVS
	if units == 'Inch Fraction' or units == 'Inch Tap':
		parent.drillsfmGB.setTitle('SFM')
		if material == 'Aluminum':
			setslider(parent, 100, 300)
			populate(parent)
		elif material == 'Brass':
			setslider(parent, 150, 300)
			populate(parent)
		elif material == 'Bronze':
			setslider(parent, 70, 150)
			populate(parent)
		elif material == 'Cast Iron':
			setslider(parent, 50, 100)
			populate(parent)
		elif material == 'Mild Steel':
			setslider(parent, 80, 110)
			populate(parent)
		elif material == 'Tool Steel':
			setslider(parent, 50, 60)
			populate(parent)
	if units == 'Metric':
		parent.drillsfmGB.setTitle('SMM')
		if material == 'Aluminum':
			setslider(parent, 30, 90)
			populate(parent)
		elif material == 'Brass':
			setslider(parent, 45, 90)
			populate(parent)
		elif material == 'Bronze':
			setslider(parent, 21, 45)
			populate(parent)
		elif material == 'Cast Iron':
			setslider(parent, 15, 30)
			populate(parent)
		elif material == 'Mild Steel':
			setslider(parent, 24, 33)
			populate(parent)
		elif material == 'Tool Steel':
			setslider(parent, 15, 18)
			populate(parent)

def setslider(parent, low, high):
	parent.drillSfmSB.setMinimum(low)
	parent.drillSfmSB.setMaximum(high)
	parent.drillSfmSB.setValue(low)

def populate(parent):
	parent.drillSfmLb.setText(str(parent.drillSfmSB.value()))
	units = parent.drillUnitsBG.checkedButton().text()
	if parent.drillMachineCB.currentData() is None:
		max_rpm = 1000000
	else:
		max_rpm = int(parent.drillMachineCB.currentData())

	#print(units)
	parent.drillChartPTE.clear()

	if units == 'Inch Fraction':
		# drillTapDrillRB
		# drillDepthBG
		# drill2xDiam
		# drill3xDiam
		# drill4xDiam
		# Reamers run in general 1/2 of drilling speed, and 2 times the drills feed.

		dia = 0.0
		parent.drillChartPTE.append('Drill\tRPM\tFeed IPM')
		for i in range(32):
			dia = dia + 0.03125
			rpm = int((3.8197 / dia) * parent.drillSfmSB.value())
			if rpm > max_rpm:
				rpm = max_rpm
			ipr = ((dia / 0.0625) * 0.001) + (parent.drilliprSB.value() * 0.001)
			ipm = ipr * rpm
			if parent.drill3xDiam.isChecked():
				rpm = int(rpm * 0.8)
				ipm = ipm * 0.8
			if parent.drill4xDiam.isChecked():
				rpm = int(rpm * 0.6)
				ipm = ipm * 0.6
			if parent.dcReamRB.isChecked():
				rpm = int(rpm * 0.5)
				ipm = ipm * 2
			parent.drillChartPTE.append(f'{dia}\t{rpm:,}\t{ipm:.1f}')
	elif units == 'Inch Tap':
		parent.drillChartPTE.append('Tap\t\tDrill\tRPM\tFeed IPM')
		for i in tapDrills:
			dia = i[2]
			rpm = int((3.8197 / dia) * parent.drillSfmSB.value())
			if rpm > max_rpm:
				rpm = max_rpm
			ipr = ((dia / 0.0625) * 0.001) + (parent.drilliprSB.value() * 0.001)
			ipm = ipr * rpm
			if parent.drill3xDiam.isChecked():
				rpm = int(rpm * 0.8)
				ipm = ipm * 0.8
			if parent.drill4xDiam.isChecked():
				rpm = int(rpm * 0.6)
				ipm = ipm * 0.6
			if parent.dcReamRB.isChecked():
				rpm = int(rpm * 0.5)
				ipm = ipm * 2
			parent.drillChartPTE.append(f'{i[0]}\t{i[1]}\t{rpm:,}\t{ipm:.1f}')


	elif units == 'Metric':
		parent.drillChartPTE.append('Diameter\tRPM\tFeed MPM')
		dia = 0
		for i in range(25):
			dia = dia + 1
			rpm = int((1000 * parent.drillSfmSB.value()) / (3.14 * dia))
			if rpm > max_rpm:
				rpm = max_rpm
			ipr = ((dia / 0.0625) * 0.001) + (parent.drilliprSB.value() * 0.001)
			ipm = ipr * rpm
			if parent.drill3xDiam.isChecked():
				rpm = int(rpm * 0.8)
				ipm = ipm * 0.8
			if parent.drill4xDiam.isChecked():
				rpm = int(rpm * 0.6)
				ipm = ipm * 0.6
			if parent.dcReamRB.isChecked():
				rpm = int(rpm * 0.5)
				ipm = ipm * 2
			parent.drillChartPTE.append(f'{dia}\t{rpm:,}\t{ipm:.1f}')

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
	cursor = parent.drillChartPTE.textCursor()
	position = cursor.position()
	cursor.select(QTextCursor.Document)
	cursor.setCharFormat(QTextCharFormat())
	cursor.clearSelection()
	cursor.setPosition(position)
	cursor.select(QTextCursor.LineUnderCursor)
	cursor.setCharFormat(fmt)
