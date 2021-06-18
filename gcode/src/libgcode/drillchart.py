tapDrills = [
['#4-40	#43', 0.0890],
['#5-40	#38', 0.1015],
['#6-32	#36', 0.1065],
['#8-32	#29', 0.1360],
['#10-24	#25', 0.1495],
['#10-32	#21', 0.1590],
['1/4-20	#7', 0.2010],
['5/16-18	F', 0.2570],
['3/8-16	5/16', 0.3125],
['7/16-14	U', 0.3680],
['1/2-13	27/64', 0.4219],
]

def update(parent):
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
	#print(units)
	parent.drillPTE.clear()

	if units == 'Inch Fraction':
		# drillTapDrillRB
		# drillDepthBG
		# drill2xDiam
		# drill3xDiam
		# drill4xDiam
		# Reamers run in general 1/2 of drilling speed, and 2 times the drills feed.

		dia = 0.0
		for i in range(32):
			dia = dia + 0.03125
			rpm = int((3.8197 / dia) * parent.drillSfmSB.value())
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
			parent.drillPTE.appendPlainText(f'{dia} \t RPM {rpm:,} \t IPM {ipm:.1f}')
	elif units == 'Inch Tap':
		for i in tapDrills:
			dia = i[1]
			rpm = int((3.8197 / dia) * parent.drillSfmSB.value())
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
			parent.drillPTE.appendPlainText(f'{i[0]} \t RPM {rpm:,} \t IPM {ipm:.1f}')


	elif units == 'Metric':
		dia = 0
		for i in range(25):
			dia = dia + 1
			rpm = int((1000 * parent.drillSfmSB.value()) / (3.14 * dia))
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
			parent.drillPTE.appendPlainText(f'{dia} \t RPM {rpm:,} \t MPM {ipm:.1f}')

