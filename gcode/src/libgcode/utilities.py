import os, configparser


def saveSettings(parent):
	settings = ['[SETTINGS]\n']
	settings.append(f'UNITS = {parent.unitsBG.checkedButton().property("units")}\n')
	settings.append(f'PREAMBLE = {parent.preambleLE.text()}\n')

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


