#!/usr/bin/python3

import serial
import sys
import numpy as np
import scipy as sp
import mat4py as m4p


def GetByte():
    a=ser.read(1)
    return ord(a)


# Define arguments to be added with the command: com_port and file to be saved
if len(sys.argv) < 3:
    print("Usage: %s <com port> <image name>.png"%sys.argv[0])
    sys.exit(0)

serport  = sys.argv[1]
fname = sys.argv[2]

#Initialize com-port
ser = serial.Serial(port=serport, baudrate=9600, bytesize=8, parity='N', stopbits=1, rtscts=1, timeout=10) # Defaults to 8-N-1

# Read and display current trace_id
ser.write(b"WFMP? WFID\r\n")
Trace_id = ser.readline().decode('utf-8').strip()
print("%s\n"%(Trace_id))

# Read and display current date
ser.write(b"WFMP? DATE\r\n")
Date = ser.readline().decode('utf-8').strip()
print("%s\n"%(Date))

# Read and display number of points x-axis
ser.write(b"WFMP? NR.\r\n")
NR_DP = ser.readline().decode('utf-8').strip()
NR_DP = int(NR_DP.split(':',1)[-1])
print("No_DP = %s\n"%(NR_DP))

# Read and display Xincr
ser.write(b"WFMP? XINCR\r\n")
Xincr = ser.readline().decode('utf-8').strip()
Xincr = float(Xincr.split(':',1)[-1])
print("Xincr = %s\n"%(Xincr))

# Read and display Xmult; multiplier x-values, only for XY-plot
ser.write(b"WFMP? XMULT\r\n")
Xmult = ser.readline().decode('utf-8').strip()
Xmult = float(Xmult.split(':',1)[-1])
print("Xmult = %s\n"%(Xmult))

# Read and display Xzero; start value x-axis
ser.write(b"WFMP? XZERO\r\n")
Xzero = ser.readline().decode('utf-8').strip()
Xzero = float(Xzero.split(':',1)[-1])
print("Xzero = %s\n"%(Xzero))

# Read and display Xunit; unit x-axis
ser.write(b"WFMP? XUNIT\r\n")
Xunit = ser.readline().decode('utf-8').strip()
Xunit = Xunit.split(':',1)[-1]
print("Xunit = %s\n"%(Xunit))

# Read and display Ymult; multiplier y-values
ser.write(b"WFMP? YMULT\r\n")
Ymult = ser.readline().decode('utf-8').strip()
Ymult = float(Ymult.split(':',1)[-1])
print("Ymult = %s\n"%(Ymult))

# Read and display Yzero; start value y-axis
ser.write(b"WFMP? YZERO\r\n")
Yzero = ser.readline().decode('utf-8').strip()
Yzero = float(Yzero.split(':',1)[-1])
print("Yzero = %s\n"%(Yzero))

# Read and display Yunit; unit y-axis
ser.write(b"WFMP? YUNIT\r\n")
Yunit = ser.readline().decode('utf-8').strip()
Yunit = Yunit.split(':',1)[-1]
print("Yunit = %s\n"%(Yunit))

# Calculate and display the x- and y-scale values per division.
Yscale = 64000*Ymult/10
m = 0
while Yscale < 1:
    Yscale = 1000*Yscale
    m += 1
Scale_y = ['V/div', 'mV/div', 'uV/div']
Yscale = int(round(Yscale))
Div_y = Scale_y[m]
Sc_y = str(Yscale) + ' ' + Div_y
    
Xscale = np.floor(NR_DP/100)*100*Xincr/10
n = 0
while Xscale < 1:
    Xscale = 1000*Xscale
    n += 1
Scale_x = ['s/div', 'ms/div', 'us/div', 'ns/div', 'ps/div', 'fs/div']
Xscale = int(Xscale)
Div_x = Scale_x[n]
Sc_x = str(Xscale) + ' ' + Div_x
 
print("Yscale = %s\n"% Sc_y)
print("Xscale = %s\n"% Sc_x)

Arr_x = np.arange(0,NR_DP,1)
Arr_x = Xzero + Xincr * Arr_x

ser.write(b"CURVE?\r\n")
Data = ser.readline().decode('utf-8').strip()
Data = Data.split(',',1)[-1]
Arr_y = np.fromstring(Data, dtype=int, sep = ',')
Arr_y = Yzero + Ymult * Arr_y
print("Arr_x = %s\n"%(Arr_x))
print("Arr_y = %s\n"%(Arr_y))

Data_mat = np.vstack([Arr_x, Arr_y])
Data_mat = np.transpose(Data_mat)
m4p.savemat(fname + '.mat', {'Data_mat' : Data_mat.tolist()})
np.savetxt(fname + '.csv',Data_mat,delimiter=',')
ser.close()


