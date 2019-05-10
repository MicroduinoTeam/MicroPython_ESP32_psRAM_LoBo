import machine

SETMODE=17
SETLEDA=18
SETLEDB=24
GETLINEA=30
GETLINEB=32
GETCOLOR=34

COLORLEDMODE=0
LINEMODE=1
COLORMODE=2

class ironManOptical(object):
    BLACK=0
    RED=1
    GREEN=2
    BLUE=3
    def __init__(self, i2c,address=0x02):
        self.devAddr = address
        self.i2c = i2c        

    def setColorLEDA(self, ar, ag, ab):
        colorledData = bytearray(6)
        colorledData[0] = ar & 0x7F
        colorledData[1] = ar >> 7
        colorledData[2] = ag & 0x7F
        colorledData[3] = ag >> 7
        colorledData[4] = ab & 0x7F
        colorledData[5] = ab >> 7
        self.i2c.writeto_mem(self.devAddr, SETMODE, bytearray([COLORLEDMODE]))
        self.i2c.writeto_mem(self.devAddr, SETLEDA, colorledData)
        
    def setColorLEDB(self, br, bg, bb):
        colorledData = bytearray(6)
        colorledData[0] = br & 0x7F
        colorledData[1] = br >> 7
        colorledData[2] = bg & 0x7F
        colorledData[3] = bg >> 7
        colorledData[4] = bb & 0x7F
        colorledData[5] = bb >> 7
        self.i2c.writeto_mem(self.devAddr, SETMODE, bytearray([COLORLEDMODE]))
        self.i2c.writeto_mem(self.devAddr, SETLEDB, colorledData)

    def setAllLED(self, cr, cg, cb):
        self.setColorLEDA(cr, cg, cb)
        self.setColorLEDB(cr, cg, cb)

    def getLine(self, colorA=RED, colorB=RED):
        #set
        self.i2c.writeto_mem(self.devAddr, SETMODE, bytearray([LINEMODE]))
        colorledline = bytearray(12)
        lineAB = bytearray(2)
        if (colorA!=self.BLACK):
          colorledline[2 * (colorA - 1)] = 1
        if (colorB!=self.BLACK):
          colorledline[6 + 2 * (colorB - 1)] = 1
        self.i2c.writeto_mem(self.devAddr, SETLEDA, colorledline)
        #get
        lineval=self.i2c.readfrom_mem(self.devAddr, GETLINEA, 4)
        lineAB[0]=lineval[1] << 7 | lineval[0]
        lineAB[1]=lineval[3] << 7 | lineval[2]
        return lineAB

