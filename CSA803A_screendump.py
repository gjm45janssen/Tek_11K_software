#!/usr/bin/python3

from PIL import Image
import serial
import sys

def GetByte():
    a=ser.read(1)
    return ord(a)

def GetData():
#   Colorpalette = {black : background; white/yellow : axes; red : trace; green : trace; magenta : trace;  turquoise : axes;  gray : menu tabs; red : stat boarders}
#    defaultPalette = [(0,0,0),(255,0,0),(140,140,140),(0,255,0),(255,255,180),(0,220,255),(0,255,255),(255,0,0)]
    defaultPalette = [(0,0,0),(255,255,180),(255,0,0),(0,255,50),(255,0,255),(0,255,255),(140,140,140),(255,0,0)]
    xRes = 552
    yRes = 704
    pixLeft = totPix = xRes * yRes # Total pixels we'll acquire
    pixList = [] # List of typles with pixel descriptors
        
    print("Receiving data (0%)")
    print("Beginning screen capture.\n")
    count = 500
    img = Image.new('RGB', (xRes, yRes), "black")
    pixels = img.load()
    x_pix = 0
    y_pix = 0
    while pixLeft > 0:
        b1 = GetByte()
        pix0 = b1 & 0x07
        pix1 = (b1 >> 3) & 0x07
#        print(pix0,pix1)
        rpt = (b1 >> 6) & 0x03
        if rpt == 0: # Repeat count actually in next byte
            rpt = GetByte()
            if rpt == 0: # Not supposed to happen
                print("Invalid data received. Continuing anyway.\n")
                #self.state = self.WaitForHeader
                #return 0
            if rpt < 4: # Repeat count >255, LSB in next byte
                rpt = (rpt << 8) + GetByte()

        if rpt > 0:	
            pixList.append((pix0,pix1,rpt))
            pixLeft -= rpt*2

        if len(pixList) == count or pixLeft == 0: # Send a block over to the GUI
            count += 500
            pd = round(float(totPix-pixLeft)/float(totPix) * 100)
            print("Receiving data (%d%%)" % pd)
        pltl = min(2*rpt, xRes-x_pix)
        for i in range(int(x_pix/2),int((x_pix+pltl)/2)):
            pixels[2*i,y_pix]=defaultPalette[pix0]
            pixels[2*i+1,y_pix]=defaultPalette[pix1]
        end = min(x_pix+pltl+1, xRes)
        for i in range(int((x_pix/2)+1),int(end/2)):
            pixels[2*i,y_pix]=defaultPalette[pix0]
            pixels[2*i+1,y_pix]=defaultPalette[pix1]
        x_pix += pltl
        if x_pix >= xRes:
            x_pix = 0
            y_pix += 1

    print("Screen capture finished.\n")
    img.show()
    img.save(fname)
    return 0


if len(sys.argv) < 3:
    print("Usage: %s <com port> <image name>.png"%sys.argv[0])
    sys.exit(0)

serport  = sys.argv[1]
fname = sys.argv[2]
ser = serial.Serial(port=serport, baudrate=9600, bytesize=8, parity='N', stopbits=1, rtscts=1, timeout=10) # Defaults to 8-N-1
print("Waiting for header. Press HARDCOPY on instrument")
strn = ser.readline().decode('utf-8').strip()
print("Instrument type and Date: %s"%strn)
xsz = ser.readline().decode('utf-8').strip()
ysz = ser.readline().decode('utf-8').strip()
print("Image Size: %s x %s\n"%(xsz,ysz))
GetData()
print("Image saved to %s"%fname)


