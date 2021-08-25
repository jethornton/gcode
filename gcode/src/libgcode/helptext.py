"""
Return text based on the tab number passed
"""

def descriptions(index):
	if index == 0:   # Setup Tab
		return text_0
	elif index == 1: # Facing Tab
		return text_1
	elif index == 2: # Pocket Tab
		return text_2
	elif index == 30: # Canned Cycles Tab
		return text_30
	elif index == 31: # G81
		return text_31
	elif index == 32: # G82
		return text_32
	elif index == 33: # G83
		return text_33
	elif index == 34: # G84
		return text_34
	elif index == 35: # G85
		return text_35
	elif index == 36: # G86
		return text_36
	elif index == 39: # G89
		return text_39
	elif index == 4: # Inputs Tab
		return text_4
	elif index == 5: # Outputs Tab
		return text_5
	elif index == 6: # Tool Changer Tab
		return text_6
	elif index == 8: # Options Tab
		return text_8
	elif index == 9: # PLC Tab
		return text_9
	elif index == 10: # Pins Tab
		return text_10
	elif index == 11: # Info Tab
		return text_11
	elif index == 12: # PC Tab
		return text_12
	elif index == 20:
		return text_20
	elif index == 30:
		return text_30
	else:
		return text_no

text_0 = """
Help Text for Setup Tab

Set default units and Preamble. Setup up to 3 machines with maximum 
spindle speed. After setting up Save Settings and they will load up
the next time you open up G code Generator
"""

text_1 = """
Help Text for Facing Tab


"""

text_2 = """
Help Text for Pocket Tab


"""


text_30 = """
Help Text for Canned Cycles Tab

Select a Canned Cycle then press F1 for help on that cycle
"""

text_31 = """
Help Text for G81 Drilling Cycle

The L (repetitions) must be 2 or more.

To use the L (repetitions) function the incremental mode (G91) must be
selected. Only one hole location must be specified. Set the start
location the distance and angle from the hole. The repeted holes will
be parallel to the path from start to the hole and the distance from
the start postion to the hole.

"""
text_32 = """
Help Text for G82 Drilling Cycle, Dwell

G82 Cycle is drilling with a dwell at the bottom of the hole.

Dwell must be specified.

The L (repetitions) must be 2 or more.

To use the L (repetitions) function the incremental mode (G91) must be
selected. Only one hole location must be specified. Set the start
location the distance and angle from the hole. The repeted holes will
be parallel to the path from start to the hole and the distance from
the start postion to the hole.
"""
text_33 = """
Help Text for G83 Peck Drilling Cycle

G83 Cycle is peck drilling with full retract to the retract position (R)
for each peck cycle.

The L (repetitions) must be 2 or more.

To use the L (repetitions) function the incremental mode (G91) must be
selected. Only one hole location must be specified. Set the start
location the distance and angle from the hole. The repeted holes will
be parallel to the path from start to the hole and the distance from
the start postion to the hole.

It is an error if:
• the Q number is negative or zero.
"""
text_34 = """
Help Text for G84 Right-hand Tapping Cycle, Dwell

G84 cycle is tapping with floating chuck and dwell at the bottom of
the hole.

The Feed rate and RPM must match the pitch of the thread.

Spindle and Dwell must be specified.

The L (repetitions) must be 2 or more.

To use the L (repetitions) function the incremental mode (G91) must be
selected. Only one hole location must be specified. Set the start
location the distance and angle from the hole. The repeted holes will
be parallel to the path from start to the hole and the distance from
the start postion to the hole.
"""
text_35 = """
Help Text for G85 Boring Cycle, Feed Out

G85 cycle is for boring or reaming

The L (repetitions) must be 2 or more.

To use the L (repetitions) function the incremental mode (G91) must be
selected. Only one hole location must be specified. Set the start
location the distance and angle from the hole. The repeted holes will
be parallel to the path from start to the hole and the distance from
the start postion to the hole.
"""
text_36 = """
Help Text for G86 Boring Cycle, Spindle Stop, Rapid Move Out

G85 cycle is for boring or reaming with spindle stopped on retract.

Spindle must be specified.

The L (repetitions) must be 2 or more.

To use the L (repetitions) function the incremental mode (G91) must be
selected. Only one hole location must be specified. Set the start
location the distance and angle from the hole. The repeted holes will
be parallel to the path from start to the hole and the distance from
the start postion to the hole.

It is an error if:
• the spindle is not turning before this cycle is executed.
"""
text_39 = """
Help Text for G89 Boring Cycle, Dwell, Feed Out

G89 cycle is for boring with a dwell at the bottom of the hole and
retract at the current feed rate.

Dwell must be specified.

The L (repetitions) must be 2 or more.

To use the L (repetitions) function the incremental mode (G91) must be
selected. Only one hole location must be specified. Set the start
location the distance and angle from the hole. The repeted holes will
be parallel to the path from start to the hole and the distance from
the start postion to the hole.
"""

text_4 = """
Help Text for Inputs Tab

Inputs are optional

If the input is a type that is associated with an axis the axis must be
specified.
"""

text_5 = """
Help Text for Outputs Tab

Outputs are optional.
"""

text_6 = """
Help Text for Tool Changer Tab

"""


text_8 = """
Help Text for Options Tab

On Screen Prompt for Manual Tool Change
	This option is if you run G code with more than one tool and the tools can be
	preset like BT and Cat holders. If you have collet type like ER and R8 you
	should not check this and you should only one tool per G code program and
	touch it off before running the program.

Hal User Interface
	This option enables halui which exports hal pins so they can be connected to
	physical or VCP or used in your hal configuration. These include pins related
	to abort, tool, spindle, program, mode, mdi, coolant, max velocity, machine,
	lube, joint, jog, feed override, rapid override, e stop, axis and home.

PyVCP Panel
	This option adds the connections and a basic PyVCP panel.

GladeVCP Panel
	Not functioning at this point.

Debug Options
	This sets the debug level that is used when an error happens. When an error
	occours the error information is sent to dmesg. Open a terminal and clear
	dmesg with sudo dmesg -c then run your configuration and to view the error
	in a terminal type dmesg.
"""

text_9 = """
Help Text for PLC Tab

Classicladder PLC will add a basic PLC to the configuration. You can also set
the number of components that Classicladder starts with.
"""
text_10 = """
Help Text for Pins Tab

If you have the 7i96 connected press get pins to get the current pinout
"""

text_11 = """
Help Text for Info Tab

Get CPU information and NIC information
"""

text_12 = """
Help Text for PC Tab

To check if the network packet time is ok get the CPU speed from the Info Tab.
Then get the tmax time and put those values into the boxes then hit calculate.
Make sure you select if the CPU speed is gHz or mHz.

To get tMax you must have the 7i96 connected to the PC and be running the
configuration with LinuxCNC.
"""

text_20 = """
Help Text for Building the Configuration

Opening the sample ini file and modifying is the fastest way to get a working configuration.
Check Configuration will scan the configuration for errors
Build Configuration will build all the configuration files needed.
	The ini file is always overwritten.
	The configName.hal file will always be overwritten.
	The tool table, variable file, postgui.hal, custom.hal, configName.clp,
	configName.xml files are never overwritten if present. To get a new one delete
	the file and a new one will be created when you build the configuration.
"""



text_no = """
No Help is found for this tab
"""

