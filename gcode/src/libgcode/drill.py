def update(parent):
	units = parent.drillUnitsBG.checkedButton().text()
	material = parent.drillMaterialBG.checkedButton().text()
	parent.drillSfmLb.setText(str(parent.drillSfmSB.value()))
	parent.drilliprLb.setText(str(parent.drilliprSB.value() * 0.001))

	# drillSfmVS
	if units == 'Imperial':
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

def sfmupdate(parent):
	parent.drillSfmLb.setText(str(parent.drillSfmSB.value()))

def populate(parent):
	units = parent.drillUnitsBG.checkedButton().text()
	parent.drillPTE.clear()

	if units == 'Imperial':
		# drillDepthBG
		# drill2xDiam
		# drill3xDiam
		# drill4xDiam
		dia = 0.0
		for i in range(16):
			dia = dia + 0.0625
			rpm = int((3.8197 / dia) * parent.drillSfmSB.value())
			ipr = ((dia / 0.0625) * 0.001) + (parent.drilliprSB.value() * 0.001)
			ipm = ipr * rpm
			if parent.drill3xDiam.isChecked():
				rpm = int(rpm * 0.8)
				ipm = ipm * 0.8
			if parent.drill4xDiam.isChecked():
				rpm = int(rpm * 0.6)
				ipm = ipm * 0.6
			parent.drillPTE.appendPlainText(f'{dia} \t RPM {rpm:,} \t IPM {ipm:.1f}')
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
			parent.drillPTE.appendPlainText(f'{dia} \t RPM {rpm:,} \t MPM {ipm:.1f}')

