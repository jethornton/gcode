==========
Installing
==========

G code Generator

.. Note:: Tested on Debian 10, no other OS is supported but it should
	work on other Debian type OS's. 

.. Note:: Requires Python 3.6 or newer to work.

Download the `deb <https://github.com/jethornton/gcode/raw/master/gcode_0.0.5_amd64.deb>`_

Or use wget from a terminal
::

	wget https://github.com/jethornton/gcode/raw/master/gcode_0.0.5_amd64.deb

If you get `bash: wget: command not found` you can install it from a terminal with
::

	sudo apt install wget

Check the readme.md file for the latest deb and md5sum.

Open the File Manager and right click on the file and open with Gdebi then install.

If you don't have Gdebi installed you can install it from a terminal
::

	sudo apt install gdebi

If you don't have LinuxCNC installed then the G code Generator
will show up in the Applications > Other menu otherwise it will be in
the CNC menu.

To uninstall the G code Generator right click on the .deb file
and open with Gdebi and select `Remove Package` or `sudo apt remove gcode`.

To upgrade the G code Generator delete the .deb file and download
a fresh copy then right click on the .deb file and open with Gdebi and
select `Reinstall Package`.
