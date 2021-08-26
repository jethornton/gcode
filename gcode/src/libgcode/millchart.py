
'''
0.125, 
0.1875, 
0.250, 
0.3125, 
0.375, 
0.500, 
0.625, 
0.750, 
1.0, 
'''

'''
3
4
5
6
8
10
12
16
20
25

'''



sample = [
['1/8"', 0.125, 0.00],
['3/16"', 0.1875, 0.00],
['1/4"', 0.250, 0.00],
['5/16"', 0.3125, 0.00],
['3/8"', 0.375, 0.00],
['1/2"', 0.500, 0.00],
['5/8"', 0.625, 0.00],
['3/4"', 0.750, 0.00],
['1"', 1.0, 0.00]
]

def update(parent):
	parent.s1018 = [
	['1/8"', 0.125, 0.0006],
	['3/16"', 0.1875, 0.0011],
	['1/4"', 0.250, 0.0017],
	['5/16"', 0.3125, 0.002],
	['3/8"', 0.375, 0.0025],
	['1/2"', 0.500, 0.0028],
	['5/8"', 0.625, 0.0032],
	['3/4"', 0.750, 0.0033],
	['1"', 1.0, 0.0041]
	]

	parent.sa2d2 = [
	['1/8"', 0.125, 0.0004],
	['3/16"', 0.1875, 0.0009],
	['1/4"', 0.250, 0.0013],
	['5/16"', 0.3125, 0.0016],
	['3/8"', 0.375, 0.0019],
	['1/2"', 0.500, 0.0021],
	['5/8"', 0.625, 0.0026],
	['3/4"', 0.750, 0.0028],
	['1"', 1.0, 0.0028]
	]

	parent.cast = [
	['1/8"', 0.125, 0.0006],
	['3/16"', 0.1875, 0.0011],
	['1/4"', 0.250, 0.0017],
	['5/16"', 0.3125, 0.002],
	['3/8"', 0.375, 0.0025],
	['1/2"', 0.500, 0.0028],
	['5/8"', 0.625, 0.0032],
	['3/4"', 0.750, 0.0033],
	['1"', 1.0, 0.0041]
	]

	parent.aluminum = [
	['1/8"', 0.125, 0.0011],
	['3/16"', 0.1875, 0.0017],
	['1/4"', 0.250, 0.0022],
	['5/16"', 0.3125, 0.0027],
	['3/8"', 0.375, 0.0032],
	['1/2"', 0.500, 0.0042],
	['5/8"', 0.625, 0.0065],
	['3/4"', 0.750, 0.0085],
	['1"', 1.0, 0.0092]
	]


	if parent.millMaterialBG.checkedButton() is None:
		#print('No Material Selected')
		return
	else:
		#material = parent.millMaterialBG.checkedButton().text()
		material = parent.millMaterialBG.checkedButton().property('material')
		sfm = parent.millMaterialBG.checkedButton().property('sfm')
		setslider(parent, sfm)
		#print(f'{material}')
		#print(f'{sfm}')
	populate(parent)

'''
Steel 1018 0.125 0.0008"  millToothsSB
'''
def populate(parent):
	parent.millSfmLb.setText(str(parent.millSfmSB.value()))
	units = parent.drillUnitsBG.checkedButton().text()
	material = parent.millMaterialBG.checkedButton().property('material')
	feeds = getattr(parent, material)
	if parent.millMachineCB.currentData() is None:
		max_rpm = 1000000
	else:
		max_rpm = int(parent.millMachineCB.currentData())

	max_rpm = int(parent.millMachineCB.currentData())
	#print(feeds)
	parent.millPTE.clear()
	parent.millPTE.appendPlainText('Size \t RPM \t IPM')
	for i in feeds:
		#print(i)
		rpm = int(parent.millSfmSB.value() * 3.82 / i[1])
		if rpm > max_rpm:
			rpm = max_rpm
		tooths = parent.millToothsSB.value()
		clf = parent.millChipLoadFactorDSB.value()
		ipt = i[2]
		ipm = rpm * tooths * clf * ipt
		parent.millPTE.appendPlainText(f'{i[0]} \t {rpm} \t {ipm:.1f}')

def setslider(parent, high):
	#parent.drillSfmSB.setMinimum(low)
	parent.millSfmSB.setMaximum(high)
	parent.millSfmSB.setValue(high)
