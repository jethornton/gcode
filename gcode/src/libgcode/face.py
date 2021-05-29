import os
from decimal import Decimal, getcontext
from PyQt5.QtWidgets import QMessageBox, QApplication, QFileDialog

def isnumber(i):
	try:
		tmp = float(i)
		return True
	except:
		return False

def retnumber(parent, i): # get line edit name then test for number
	if getattr(parent, i).text():
		try:
			num = float(getattr(parent, i).text())
			return num
		except Exception as e:
			print(e)
			name = getattr(parent, i).property("name")
			text = getattr(parent, i).text()
			print(i)
			parent.errorMsgOk(f'{name} {text} is not a number', 'Error')
			#print(f'{parent.faceWidthX.property("name")} is not a number')
			return False

def generate(parent):
	"""
	It is recommended that you program a tool path that keeps the milling cutter
	in full contact, rather than performing several parallel passes. When changing
	direction, include a small radial tool path to keep the cutter moving and
	constantly engaged

	start X face left - leadin
	cutter diamter / 2 is center 
	1" cutter 0.5" center -0.25" path is for 25%
	stepover cutter diameter * percent
	start Y = face rear minus cutter radius + step
	end X = width X + step * 2
	G2 arc X position + radius Y position - radius I0 J- radius
	X 9.5 
	X 9.5 + 0.5 Y-0.25 + 0.5 I0.0 jJ 9.5 - 0.5
	G2
	stock size decrease in size as cut
	
	initial cut path = radius - cutwidth
	I X offset relative
	J Y offset relative
	X10 Y5
	T5 M6 G43
	F25 S1800
	;leadin
	G0 X-0.5 Y0.1875
	1 G1 X10.0 Y0.1875
	2 G2 X10.1875 Y0.0 I0.0 J-0.1875
	3 G1 X10.1875 Y-5.0
	4 G2 X10.0 Y-5.1875 I-0.1875 J0.0
	5 G1 X0.0 Y-5.1875
	6 G2 X-0.1875 Y-5.0 I0.0 J0.1875
	7 G1 X-0.1875 Y-0.1875
	; second loop last positions - cutwidth
	8 G2 X0.0 Y0.0 I0.1875 J0.0
	"""
	widthX = retnumber(parent, 'faceWidthX')
	depthY = retnumber(parent, 'faceDepthY')
	left = retnumber(parent, 'faceLeft')
	back = retnumber(parent, 'faceRear')
	top = retnumber(parent, 'faceTop')
	tool = retnumber(parent, 'faceTool')
	diam = retnumber(parent, 'faceToolDia')
	radius = diam / 2
	rpm = retnumber(parent, 'faceRPM')
	feed = retnumber(parent, 'faceFeed')
	stepPercent = retnumber(parent, 'faceStep') * 0.01
	safeZ = retnumber(parent, 'faceSafeZ')
	leadin = retnumber(parent, 'faceLeadIn')
	cutdepth = -retnumber(parent, 'faceCutDepth')
	print(cutdepth)
	stepdepth = retnumber(parent, 'faceStepDepth')

	step = min(widthX, depthY)
	cutwidth = diam * stepPercent

	steps = int(round((min(widthX, depthY) + (2 * cutwidth)) / cutwidth, 0)/2)
	print(steps)

	# setup initial path ends
	# end + radius - cutwidth = path
	plusX = (left + widthX) + radius - cutwidth
	minusX = left - radius + cutwidth
	plusY = back + radius - cutwidth
	minusY = (back - depthY) - radius + cutwidth

	parent.facePTE.clear()
	parent.facePTE.appendPlainText(f';Face Stock X{left} to X{left + widthX} '
		f'Y{back} to Y{back - depthY}')
	parent.facePTE.appendPlainText(f';Inital Path X{minusX - leadin} '
		f'Y{plusY} to X{plusX} to Y{minusY} to X{minusX} to Y{plusY - cutwidth}')
	parent.facePTE.appendPlainText(f'G0 Z{safeZ}')

	if tool:
		parent.facePTE.appendPlainText(f'T{int(tool)} M6 G43')
	parent.facePTE.appendPlainText(f'G0 X{minusX  - leadin} Y{plusY}')
	parent.facePTE.appendPlainText(f'M3 S{rpm} F{feed}')
	#parent.facePTE.appendPlainText(f'G0 Z{top + 0.250}')
	currentZ = top

	# depth loop
	while currentZ > cutdepth:
		parent.facePTE.appendPlainText(f'G0 Z{safeZ}')

		plusX = (left + widthX) + radius - cutwidth
		minusX = left - radius + cutwidth
		plusY = back + radius - cutwidth
		minusY = (back - depthY) - radius + cutwidth
		parent.facePTE.appendPlainText(f'G0 X{minusX  - leadin} Y{plusY}')

		nextZ = currentZ - stepdepth
		parent.facePTE.appendPlainText(f'G1 Z{nextZ}')
		currentZ = nextZ

		# path loop
		for i in range(steps):
			parent.facePTE.appendPlainText(f'G1 X{plusX - cutwidth} Y{plusY} ; 1')
			plusY = plusY - cutwidth
			parent.facePTE.appendPlainText(f'G2 X{plusX} Y{plusY} I0.0 J-{cutwidth} ; 2')
			parent.facePTE.appendPlainText(f'G1 X{plusX} Y{minusY + cutwidth} ; 3')
			plusX = plusX - cutwidth
			parent.facePTE.appendPlainText(f'G2 X{plusX} Y{minusY} I-{cutwidth} J0.0 ; 4')
			parent.facePTE.appendPlainText(f'G1 X{minusX + cutwidth} Y{minusY} ; 5')
			minusY = minusY + cutwidth
			w = plusX - minusX
			d = plusY - minusY
			#print(f'pass {i} width left {w} depth left{d}')
			if d <= 0.0 or w <= 0.0: break
			parent.facePTE.appendPlainText(f'G2 X{minusX} Y{minusY} I0.0 J{cutwidth} ; 6')
			parent.facePTE.appendPlainText(f'G1 X{minusX} Y{plusY - cutwidth} ; 7')
			minusX = minusX + cutwidth
			parent.facePTE.appendPlainText(f'G2 X{minusX} Y{plusY} I{cutwidth} J0.0 ; 8')
			parent.facePTE.appendPlainText(f'; +X{plusX} -X{minusX} +Y{plusY} -Y{minusY}')
		parent.facePTE.appendPlainText(f'G0 Z{safeZ}')
	parent.facePTE.appendPlainText('M2')

	# parent.facePTE.appendPlainText(f'{}')

def copy(parent):
	qclip = QApplication.clipboard()
	qclip.setText(parent.facePTE.toPlainText())
	parent.statusbar.showMessage('G code copied to clipboard')

def save(parent):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		ncDir = os.path.join(os.path.expanduser("~"), 'linuxcnc/nc_files')
		fileName, _ = QFileDialog.getSaveFileName(parent,
		caption="Save File", directory=ncDir,
		filter="All Files (*);;G Code Files (*.ngc)", options=options)
		if fileName:
			with open(fileName, 'w') as f:
				f.writelines(parent.facePTE.toPlainText())

def GenCode(self):
	""" Generate the G-Code for facing a part 
	assume that the part is at X0 to X+, Y0 to Y-"""
	pass
	D=Decimal
	z=float(self.SafeZVar.get())
	# Calculate the start position 1/2 the tool diameter + 0.100 in X and Stepover in Y
	self.ToolRadius = self.FToD(self.ToolDiameterVar.get())/2
	if len(self.LeadinVar.get())>0:
			self.LeadIn = self.FToD(self.LeadinVar.get())
	else:
			self.LeadIn = self.ToolRadius + D('0.1')
	self.X_Start = -(self.LeadIn)
	self.X_End = self.FToD(self.PartLengthVar.get()) + self.LeadIn
	if len(self.StepOverVar.get())>0:
			self.Y_StepOver = (self.FToD(self.ToolDiameterVar.get())\
					* self.FToD(self.StepOverVar.get())/100)
	else:
			self.Y_StepOver = self.FToD(self.ToolDiameterVar.get())*D('.75')
	if self.HomeVar.get()==4:
		self.Y_Start = (self.ToolRadius - self.Y_StepOver)
		self.Y_End = -(self.FToD(self.PartWidthVar.get())-\
					(self.ToolRadius - self.Y_StepOver))+D('.1')
	else:
		self.Y_Start = -(self.ToolRadius - self.Y_StepOver)
		self.Y_End = (self.FToD(self.PartWidthVar.get())+\
					(self.ToolRadius + self.Y_StepOver))+D('.1')
	self.Z_Total = self.FToD(self.TotalToRemoveVar.get())
	if len(self.DepthOfCutVar.get())>0:
			self.Z_Step = self.FToD(self.DepthOfCutVar.get())
			self.NumOfZSteps = int(self.FToD(self.TotalToRemoveVar.get()) / self.Z_Step)
			if self.Z_Total % self.Z_Step > 0:
					self.NumOfZSteps = self.NumOfZSteps + 1
	else:
			self.Z_Step = 0
			self.NumOfZSteps = 1
	self.NumOfYSteps = int(ceil(self.FToD(self.PartWidthVar.get())/self.Y_StepOver))
	self.Z_Position = 0
	# Generate the G-Codes
	if self.UnitVar.get()==1:
			self.g_code.insert(END, 'G20 ')
	else:
			self.g_code.insert(END, 'G21 ')
	if len(self.SpindleRPMVar.get())>0:
			self.g_code.insert(END, 'S%i ' %(self.FToD(self.SpindleRPMVar.get())))
			self.g_code.insert(END, 'M3 ')
	if len(self.FeedrateVar.get())>0:
			self.g_code.insert(END, 'F%s\n' % (self.FeedrateVar.get()))
	for i in range(self.NumOfZSteps):
			self.g_code.insert(END, 'G0 X%.4f Y%.4f\nZ%.4f\n' \
					%(self.X_Start, self.Y_Start,z))
			# Make sure the Z position does not exceed the total depth
			if self.Z_Step>0 and (self.Z_Total+self.Z_Position) >= self.Z_Step:
					self.Z_Position = self.Z_Position - self.Z_Step
			else:
					self.Z_Position = -self.Z_Total
			self.g_code.insert(END, 'G1 Z%.4f\n' % (self.Z_Position))
			self.X_Position = self.X_Start
			self.Y_Position = self.Y_Start

			for i in range(self.NumOfYSteps):
					if self.X_Position == self.X_Start: 
							self.g_code.insert(END, 'G1 X%.4f\n' % (self.X_End))
							self.X_Position = self.X_End
					else:
							self.g_code.insert(END, 'G1 X%.4f\n' % (self.X_Start))
							self.X_Position = self.X_Start
					if self.HomeVar.get()==4:
							self.Y_Position = self.Y_Position - self.Y_StepOver
					else:
							self.Y_Position = self.Y_Position + self.Y_StepOver
					if self.HomeVar.get()==4:
							if self.Y_Position > self.Y_End:
									self.g_code.insert(END, 'G0 Y%.4f\n' % (self.Y_Position))
					else:
							if self.Y_Position < self.Y_End:
									self.g_code.insert(END, 'G0 Y%.4f\n' % (self.Y_Position))
	self.g_code.insert(END, 'G0 Z%.4f\n'% z)
	if len(self.SpindleRPMVar.get())>0:
			self.g_code.insert(END, 'M5\n')
	self.g_code.insert(END, 'G0 X0.0000 Y0.0000\nM2 (End of File)\n')

def FToD(self,s): # Float To Decimal
		"""
		Returns a decimal with 4 place precision
		valid imputs are any fraction, whole number space fraction
		or decimal string. The input must be a string!
		"""
		s=s.strip(' ') # remove any leading and trailing spaces
		D=Decimal # Save typing
		P=D('0.0001') # Set the precision wanted
		if ' ' in s: # if it is a whole number with a fraction
				w,f=s.split(' ',1)
				w=w.strip(' ') # make sure there are no extra spaces
				f=f.strip(' ')
				n,d=f.split('/',1)
				return D(D(n)/D(d)+D(w)).quantize(P)
		elif '/' in s: # if it is just a fraction
				n,d=s.split('/',1)
				return D(D(n)/D(d)).quantize(P)
		return D(s).quantize(P) # if it is a decimal number already

def GetIniData(self,FileName,SectionName,OptionName,default=''):
		"""
		Returns the data in the file, section, option if it exists
		of an .ini type file created with ConfigParser.write()
		If the file is not found or a section or an option is not found
		returns an exception
		"""
		self.cp=ConfigParser()
		try:
				self.cp.readfp(open(FileName,'r'))
				try:
						self.cp.has_section(SectionName)
						try:
								IniData=self.cp.get(SectionName,OptionName)
						except:
								IniData=default
				except:
						IniData=default
		except:
				IniData=default
		return IniData
		
def WriteIniData(self,FileName,SectionName,OptionName,OptionData):
		"""
		Pass the file name, section name, option name and option data
		When complete returns 'sucess'
		"""
		self.cp=ConfigParser()
		try:
				self.fn=open(FileName,'a')
		except IOError:
				self.fn=open(FileName,'w')
		if not self.cp.has_section(SectionName):
				self.cp.add_section(SectionName)
		self.cp.set(SectionName,OptionName,OptionData)
		self.cp.write(self.fn)
		self.fn.close()

def GetDirectory(self):
		self.DirName = askdirectory(initialdir='/home',title='Please select a directory')
		if len(self.DirName) > 0:
				return self.DirName 
	 
def CopyClpBd(self):
		self.g_code.clipboard_clear()
		self.g_code.clipboard_append(self.g_code.get(0.0, END))

def WriteToFile(self):
		self.NewFileName = asksaveasfile(initialdir=self.NcDir,mode='w', \
master=self.master,title='Create NC File',defaultextension='.ngc')
		self.NcDir=os.path.dirname(self.NewFileName.name)
		self.NewFileName.write(self.g_code.get(0.0, END))
		self.NewFileName.close()

def LoadPrefs(self):
		self.NcDir=self.GetIniData('face.ini','Directories','NcFiles',os.path.expanduser("~"))
		self.FeedrateVar.set(self.GetIniData('face.ini','MillingPara','Feedrate','1000'))
		self.DepthOfCutVar.set(self.GetIniData('face.ini','MillingPara','DepthOfCut','3'))
		self.ToolDiameterVar.set(self.GetIniData('face.ini','MillingPara','ToolDiameter','10'))
		self.SpindleRPMVar.set(self.GetIniData('face.ini','MillingPara','SpindleRPM','9000'))
		self.StepOverVar.set(self.GetIniData('face.ini','MillingPara','StepOver','50'))
		self.LeadinVar.set(self.GetIniData('face.ini','MillingPara','Leadin'))
		self.UnitVar.set(int(self.GetIniData('face.ini','MillingPara','UnitVar','2')))
		self.HomeVar.set(int(self.GetIniData('face.ini','MillingPara','HomeVar','4')))
		self.SafeZVar.set(self.GetIniData('face.ini','MillingPara','SafeZ','10.0'))
		self.PartLengthVar.set(self.GetIniData('face.ini','Part','X'))
		self.PartWidthVar.set(self.GetIniData('face.ini','Part','Y'))
		self.TotalToRemoveVar.set(self.GetIniData('face.ini','Part','TotalToRemove'))


def SavePrefs(self):
		def set_pref(SectionName,OptionName,OptionData):
				if not self.cp.has_section(SectionName):
						self.cp.add_section(SectionName)
				self.cp.set(SectionName,OptionName,OptionData)
		self.cp=ConfigParser()
		self.fn=open('face.ini','w')
		set_pref('Directories','NcFiles',self.NcDir)
		set_pref('MillingPara','Feedrate',self.FeedrateVar.get())
		set_pref('MillingPara','DepthOfCut',self.DepthOfCutVar.get())
		set_pref('MillingPara','ToolDiameter',self.ToolDiameterVar.get())
		set_pref('MillingPara','SpindleRPM',self.SpindleRPMVar.get())
		set_pref('MillingPara','StepOver',self.StepOverVar.get())
		set_pref('MillingPara','Leadin',self.LeadinVar.get())
		set_pref('MillingPara','UnitVar',self.UnitVar.get())
		set_pref('MillingPara','HomeVar',self.HomeVar.get())
		set_pref('MillingPara','SafeZ',self.SafeZVar.get())
		set_pref('Part','X',self.PartLengthVar.get())
		set_pref('Part','Y',self.PartWidthVar.get())
		set_pref('Part','TotalToRemove',self.TotalToRemoveVar.get())
		self.cp.write(self.fn)
		self.fn.close()

def Simple(self):
		tkMessageBox.showinfo('Feature', 'Sorry this Feature has\nnot been programmed yet.')

def ClearTextBox(self):
		self.g_code.delete(1.0,END)

def SelectAllText(self):
		self.g_code.tag_add(SEL, '1.0', END)

def SelectCopy(self):
		self.SelectAllText()
		self.CopyClpBd()

