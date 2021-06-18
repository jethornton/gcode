def spot(parent):
	pass

def drill(parent):
	cursor = parent.drillPTE.textCursor()
	info = cursor.selectedText().split()
	parent.drillRpmLE.setText(info[2])
	parent.drillFeedLE.setText(info[4])
