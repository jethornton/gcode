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
			parent.drillPTE.clear()
			parent.drillPTE.appendPlainText('Metric Not Programmed Yet')
		elif material == 'Brass':
			parent.drillPTE.clear()
			parent.drillPTE.appendPlainText('Metric Not Programmed Yet')
		elif material == 'Bronze':
			parent.drillPTE.clear()
			parent.drillPTE.appendPlainText('Metric Not Programmed Yet')
		elif material == 'Cast Iron':
			parent.drillPTE.clear()
			parent.drillPTE.appendPlainText('Metric Not Programmed Yet')
		elif material == 'Mild Steel':
			parent.drillPTE.clear()
			parent.drillPTE.appendPlainText('Metric Not Programmed Yet')
		elif material == 'Tool Steel':
			parent.drillPTE.clear()
			parent.drillPTE.appendPlainText('Metric Not Programmed Yet')

def setslider(parent, low, high):
	parent.drillSfmSB.setMinimum(low)
	parent.drillSfmSB.setMaximum(high)
	parent.drillSfmSB.setValue(low)

def sfmupdate(parent):
	parent.drillSfmLb.setText(str(parent.drillSfmSB.value()))

def populate(parent):
	parent.drillPTE.clear()
	dia = 0.0
	for i in range(16):
		dia = dia + 0.0625
		rpm = int((3.8197 / dia) * parent.drillSfmSB.value())
		ipr = ((dia / 0.0625) * 0.001) + (parent.drilliprSB.value() * 0.001)
		ipm = ipr * rpm
		parent.drillPTE.appendPlainText(f'{dia} \t RPM {rpm:,} \t IPM {ipm:.1f}')
