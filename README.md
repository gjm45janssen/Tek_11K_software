# Tek_CSA803A_software
Some Python programs to download data from CSA803A Tektronix scope.

This software runs under Python. The version I use is 3.7.1.

1. CSA803A_screendump.py

This program is strongly based on the screendump software using the serial interface, written by Gudjon Gudjonsson:  https://github.com/GauiStori/tekprogs/tree/master/csa803c/utils .
However, I found a small bug in the image decoding part of this software, which caused pixels to be mixed up resulting in distorted letters sometimes.

For the screendump program to work, the following modules need to be installed:
- pillow
- pyserial
The modules are installed with the command: 
pip install (–-user) <module>

You run the software as follows:

python CSA803A_screendump.py <com-port> <filename>

Here <com-port> = COM1, COM2, etc. whichever serial port is connected with the scope. 
The RS232C com-port settings are as in the image com-port.png.
The ‘Hardcopy’ settings are as in hardcopy.png image.
<filename> is the name of the file to which the image is written. The extension can be ‘png’ (Portable Network Graphic), which is a compressed file and therefore smaller in size, or ‘bmp’ for a bitmap image file (much larger).
In the ‘defaultPalette’ you may adapt the different colors to your liking.
This software was tested and runs with a CSA803A and 11403A. It did not run with an 11402, which only sends the screen image to the printer port.


2. CSA803A_trace_data.py and CSA803A_trace-persist_data.py

These programs send the data of the actual written curve via the serial port to the PC and writes it in two separate files in CVS format (extension ‘cvs’) and Matlab format (extension ‘mat’). This allows for processing of the samples by yourself.

For the data download program to work, the following modules need to be installed:
- numpy
- scipy
- mat4py
- pyserial

When in ‘Display Modes’ => ‘Persist/Histogram’ the ‘Normal’ setting is selected, CSA803A_trace.py should be used, and the stored file contains two columns: X-data and Y-data. The data is scaled according to the settings of the oscilloscope.
When in ‘Display Modes’ => ‘Persist/Histogram’ the ‘Variable’ persistence setting is selected, CSA803A_trace-persist.py should be used. Now the stored file contains N+1 columns: one X-data and N Y-data columns. The number of y-data columns depends on the persistence-time chosen. For a longer persistence-time the data of all curves that are used to calculate the shown scope image is written as Y-data columns. Note that the number of Y-data columns increases quite rapidly with increased persistence-time causing a longer download time.

You run the software as follows:

python CSA803A_trace*.py <com-port> <filename>

Here <com-port> = COM1, COM2, etc. whichever serial port is connected with the scope. 
The RS232C com-port settings are as in the image com-port.png.
<filename> is the name of the data file without extension.
This software was tested and runs with a CSA803A. I expect it to run with a CSA803C and 11801B/C as well.

