import os, configparser
from PyQt5.QtWidgets import (QLineEdit, QSpinBox, QCheckBox, QComboBox,
	QLabel, QGroupBox, QDoubleSpinBox)

ini_options = [
	['SETTINGS', 'UNITS', 'unitsBG'],
	['SETTINGS', 'PREAMBLE', 'preambleLE'],
	['SETTINGS', 'NAME_0', 'machineLE_0'],
	['SETTINGS', 'MAX_RPM_0', 'machineMaxSB_0'],
	['SETTINGS', 'NAME_1', 'machineLE_1'],
	['SETTINGS', 'MAX_RPM_1', 'machineMaxSB_1'],
	['SETTINGS', 'NAME_2', 'machineLE_2'],
	['SETTINGS', 'MAX_RPM_2', 'machineMaxSB_2'],
	]

def saveSettings(parent):
	settings = ['[SETTINGS]\n']
	settings.append(f'UNITS = {parent.unitsBG.checkedButton().property("units")}\n')
	settings.append(f'PREAMBLE = {parent.preambleLE.text().strip()}\n')
	settings.append(f'NAME_0 = {parent.machineLE_0.text().strip()}\n')
	settings.append(f'MAX_RPM_0 = {parent.machineMaxSB_0.value()}\n')
	settings.append(f'NAME_1 = {parent.machineLE_1.text().strip()}\n')
	settings.append(f'MAX_RPM_1 = {parent.machineMaxSB_1.value()}\n')
	settings.append(f'NAME_2 = {parent.machineLE_2.text().strip()}\n')
	settings.append(f'MAX_RPM_2 = {parent.machineMaxSB_2.value()}\n')

	sf = os.path.expanduser('~/.gcode_settings')
	with open(sf, 'w') as f:
		f.writelines(settings) 

def getSettings(parent):
	sf = os.path.expanduser('~/.gcode_settings')
	if os.path.isfile(sf):
		config = configparser.ConfigParser(strict=False)
		config.optionxform = str
		config.read(sf)

		for item in ini_options:
			if config.has_option(item[0], item[1]):
				if isinstance(getattr(parent, item[2]), QLabel):
					getattr(parent, item[2]).setText(config[item[0]][item[1]])
				if isinstance(getattr(parent, item[2]), QLineEdit):
					getattr(parent, item[2]).setText(config[item[0]][item[1]])
				if isinstance(getattr(parent, item[2]), QSpinBox):
					getattr(parent, item[2]).setValue(abs(int(config[item[0]][item[1]])))
				if isinstance(getattr(parent, item[2]), QDoubleSpinBox):
					getattr(parent, item[2]).setValue(float(config[item[0]][item[1]]))
				if isinstance(getattr(parent, item[2]), QCheckBox):
					getattr(parent, item[2]).setChecked(eval(config[item[0]][item[1]]))
				if isinstance(getattr(parent, item[2]), QGroupBox):
					getattr(parent, item[2]).setChecked(eval(config[item[0]][item[1]]))
					#print(self.config[item[0]][item[1]])
				if isinstance(getattr(parent, item[2]), QComboBox):
					index = getattr(v, item[2]).findData(config[item[0]][item[1]])
					if index >= 0:
						getattr(parent, item[2]).setCurrentIndex(index)

		for i in range(3):
			#print(parent.machineLE_0.text())
			#print(getattr(parent, 'machineLE_' + str(i)).text())
			# getattr(self, 'minLimit_' + str(i)).setToolTip('inches')
			#print(getattr(parent, 'machineLE_') + str(i)).text()
			machine = getattr(parent, 'machineLE_' + str(i)).text()
			rpm = getattr(parent, 'machineMaxSB_' + str(i)).text()
			getattr(parent, 'drillMachineCB').addItem(machine, rpm)
			getattr(parent, 'millMachineCB').addItem(machine, rpm)
			#parent.drillMachineCB.addItem

	'''
		if config.has_section('SETTINGS'):
			for i in items:
				if config.has_option(i[0], i[1]):
					print(i)
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
	'''
