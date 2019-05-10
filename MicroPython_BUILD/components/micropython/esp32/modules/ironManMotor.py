import machine,time

BIT_13 = 13
BIT_12 = 12
BIT_11 = 11
BIT_10 = 10
BIT_9 = 9
BIT_8 = 8

CLOSEMAXSPEED = 500

ADDR8_RESET = 6
ADDR16_SET_SPEED = 22
ADDR8_MODE = 28
ADDR16_SPD_KP = 30
ADDR16_SPD_KI = 32
ADDR16_SPD_KD = 34

class ironManMotor(object):
  BRAKE=16383
  FREE=0
  
  MODE_OPEN = 0x00
  MODE_SPEED = 0x01
  MODE_POSITION = 0x02
  
  def __init__(self, i2c,address=0x04, _bit=BIT_8):
    self.i2c = i2c 
    self.devAddr = address
    _bit = self.constrain(_bit, BIT_8, BIT_13)
    self.multiple = 0x2000 >> _bit
    self.speedRange = 1 << _bit - 1
    
    time.sleep(2)
    
  def constrain(self, val, min_val, max_val):
    if val < min_val:
        return min_val
    if val > max_val:
        return max_val
    return val
    
  def map(self, x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
  def writeInt16(self, dataaddr, data):
     _data16 = data
     if ((_data16 > 0x1fff) and (_data16 < self.BRAKE)):
       _data16 = data + 0x3fff
     self.i2c.writeto_mem(self.devAddr, dataaddr, bytearray([_data16 & 0x7F,(_data16 >> 7) & 0x7F]))
    
  def reset(self):
    self.i2c.writeto_mem(self.devAddr, ADDR8_RESET, bytearray([1]))
    
  def setRatio(self, _ratio):
    self.ratio = _ratio
    
  def setResolution(self, _resolution):
    self.resolution = _resolution
    
  def setMode(self, _mode):
    self.motorMode=_mode
    self.i2c.writeto_mem(self.devAddr, ADDR8_MODE, bytearray([1]))
    
  def setS_PID_P(self, skp):
    self.i2c.writeto_mem(self.devAddr, ADDR16_SPD_KP, bytearray([skp & 0x7F,(skp >> 7) & 0x7F]))
    
  def setS_PID_I(self, ski):
    self.i2c.writeto_mem(self.devAddr, ADDR16_SPD_KI, bytearray([ski & 0x7F,(ski >> 7) & 0x7F]))
    
  def setS_PID_D(self, skd):
    self.i2c.writeto_mem(self.devAddr, ADDR16_SPD_KD, bytearray([skd & 0x7F,(skd >> 7) & 0x7F]))
    
  def setSpeed(self, speed):
    if(speed==self.BRAKE):
      speedBuf = speed 
    else:
      if(self.motorMode==self.MODE_OPEN):
        if(self.multiple==0x20):
          speed = self.constrain(speed, -255, 255)
        elif(self.multiple==0x10):
          speed = self.constrain(speed, -551, 551)
        elif(self.multiple==0x8):
          speed = self.constrain(speed, -1023, 1023)
        elif(self.multiple==0x4):
          speed = self.constrain(speed, -2047, 2047)
        elif(self.multiple==0x2):
          speed = self.constrain(speed, -4095, 4095)
        elif(self.multiple==0x1):
          speed = self.constrain(speed, -8191, 8191)
        speedBuf = speed * self.multiple
      else:
        if(speed > 255):
          _speed = CLOSEMAXSPEED
        elif(speed < -255):
          _speed = -CLOSEMAXSPEED
        else:
          _speed = self.map(speed,-255,255,-CLOSEMAXSPEED,CLOSEMAXSPEED)
        if(_speed==0):
          speedBuf = self.BRAKE
        else:
          _speedBuf = _speed / 100.0
          speedBuf = int(self.ratio * self.resolution * _speedBuf)
      self.writeInt16(ADDR16_SET_SPEED, speedBuf)

