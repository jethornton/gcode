import os, configparser


def saveSettings(parent):
	settings = ['[SETTINGS]\n']
	settings.append(f'UNITS = {parent.unitsBG.checkedButton().property("units")}\n')
	settings.append(f'PREAMBLE = {parent.preambleLE.text()}\n')
	settings.append(f'NAME_1 = {parent.machine1LE.text()}\n')
	settings.append(f'MAX_RPM_1 = {parent.machine1MaxSB.value()}\n')
	settings.append(f'NAME_2 = {parent.machine2LE.text()}\n')
	settings.append(f'MAX_RPM_2 = {parent.machine2MaxSB.value()}\n')
	settings.append(f'NAME_3 = {parent.machine3LE.text()}\n')
	settings.append(f'MAX_RPM_3 = {parent.machine3MaxSB.value()}\n')
	

	sf = os.path.expanduser('~/.gcode_settings')
	with open(sf, 'w') as f:
		f.writelines(settings) 

def getSettings(parent):
	sf = os.path.expanduser('~/.gcode_settings')
	if os.path.isfile(sf):
		config = configparser.ConfigParser(strict=False)
		config.optionxform = str
		config.read(sf)
		if config['SETTINGS']['UNITS'] == 'G20':
			parent.inchRB.setChecked(True)
		else:
			parent.mmRB.setChecked(True)
		parent.preambleLE.setText(config['SETTINGS']['PREAMBLE'])
		parent.machine1LE.setText(config['SETTINGS']['NAME_1'])
		parent.machine1MaxSB.setValue(int(config['SETTINGS']['MAX_RPM_1']))
		parent.machine2LE.setText(config['SETTINGS']['NAME_2'])
		parent.machine2MaxSB.setValue(int(config['SETTINGS']['MAX_RPM_2']))
		parent.machine3LE.setText(config['SETTINGS']['NAME_3'])
		parent.machine3MaxSB.setValue(int(config['SETTINGS']['MAX_RPM_3']))

		parent.drillMachineCB.addItem(config['SETTINGS']['NAME_1'], config['SETTINGS']['MAX_RPM_1'])
		parent.drillMachineCB.addItem(config['SETTINGS']['NAME_2'], config['SETTINGS']['MAX_RPM_2'])
		parent.drillMachineCB.addItem(config['SETTINGS']['NAME_3'], config['SETTINGS']['MAX_RPM_3'])

		parent.millMachineCB.addItem(config['SETTINGS']['NAME_1'], config['SETTINGS']['MAX_RPM_1'])
		parent.millMachineCB.addItem(config['SETTINGS']['NAME_2'], config['SETTINGS']['MAX_RPM_2'])
		parent.millMachineCB.addItem(config['SETTINGS']['NAME_3'], config['SETTINGS']['MAX_RPM_3'])

# drillMachineCB

# millMachineCB
