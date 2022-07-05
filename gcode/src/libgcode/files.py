import os

from PyQt5.QtWidgets import QFileDialog

def saveFilePath(parent, extension):
	if os.path.exists(parent.templateLocationLE.text()):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		templateDir = parent.templateLocationLE.text()
		fileName, _ = QFileDialog.getSaveFileName(parent,
		caption="Save File", directory=templateDir,
		filter=f"Facing Templates (*.{extension})", options=options)
	else:
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		templateDir = os.path.expanduser("~")
		fileName, _ = QFileDialog.getSaveFileName(parent,
		caption="Save File", directory=templateDir,
		filter=f"Facing Templates (*.{extension})", options=options)
	if fileName:
		path, ext = os.path.splitext(fileName)
		if ext == '':
			#print(f'{fileName}')
			return(f'{fileName}.{extension}')
		else:
			#print(f'{fileName}')
			return(f'{fileName}')
	else:
		return(False)


def openFile(parent,extension):
	if os.path.exists(parent.templateLocationLE.text()):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		templateDir = parent.templateLocationLE.text()
		fileName, _ = QFileDialog.getOpenFileName(parent,
		caption="Save File", directory=templateDir,
		filter=f"Facing Templates (*.{extension})", options=options)
	else:
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		templateDir = os.path.expanduser("~")
		fileName, _ = QFileDialog.getOpenFileName(parent,
		caption="Save File", directory=templateDir,
		filter=f"Facing Templates (*.{extension})", options=options)
	if fileName:
		path, ext = os.path.splitext(fileName)
		if ext == '':
			print(f'{fileName}')
			return(f'{fileName}.{extension}')
		else:
			print(f'{fileName}')
			return(f'{fileName}')
	else:
		return(False)

