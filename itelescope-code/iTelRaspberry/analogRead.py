# read abelectronics ADC Pi V2 board inputs on channel 7 & 8.
# Requries Python 2.7
# Requires SMBus 
# I2C API depends on I2C support in the kernel

from smbus import SMBus
import re

class analogRead(object):
    def __init__(self):
        self.adc_address1 = 0x68
        self.adc_address2 = 0x69
        
        # create byte array and fill with initial values to define size
        self.adcreading = bytearray()
        
        self.adcreading.append(0x00)
        self.adcreading.append(0x00)
        self.adcreading.append(0x00)
        self.adcreading.append(0x00)
        
        self.setDivisor(64)
        #self.varDivisior = 64 # default value: from pdf sheet on adc addresses and config
        #self.varMultiplier = (2.4705882/self.varDivisior)/1000

        # detect i2C port number and assign to i2c_bus
        for line in open('/proc/cpuinfo').readlines():
            m = re.match('(.*?)\s*:\s*(.*)', line)
            if m:
                (name, value) = (m.group(1), m.group(2))
                if name == "Revision":
                    if value [-4:] in ('0002', '0003'):
                        i2c_bus = 0
                    else:
                        i2c_bus = 1
                    break
                       
        
        self.bus = SMBus(i2c_bus)
 
    def changechannel(self, address, adcConfig):
        tmp = self.bus.write_byte(address, adcConfig)

    def getadcreading(self, address, adcConfig):
        adcreading = self.bus.read_i2c_block_data(address,adcConfig)
        h = adcreading[0]
        m = adcreading[1]
        l = adcreading[2]
        s = adcreading[3]
        # wait for new data
        while (s & 128):
            adcreading = self.bus.read_i2c_block_data(address,adcConfig)
            h = adcreading[0]
            m = adcreading[1]
            l = adcreading[2]
            s = adcreading[3]
        
        # shift bits to product result
        t = ((h & 0b00000001) << 16) | (m << 8) | l
        # check if positive or negative number and invert if needed
        if (h > 128):
            t = ~(0x020000 - t)
        return t * self.varMultiplier
        
    def readChannelSeven(self):
        return self.readCSeven18bit()
    
    def readChannelEight(self):
        return self.readCEight18bit()
    
    def setDivisor(self,div):
        self.varDivisior = div # default value: from pdf sheet on adc addresses and config
        self.varMultiplier = (2.4705882/self.varDivisior)/1000
        
    def readCSeven18bit(self):
        self.setDivisor(64)
        self.changechannel(self.adc_address2, 0xDC)
        return self.getadcreading(self.adc_address2, 0xDC)
    
    def readCSeven16bit(self):
        self.setDivisor(16)
        self.changechannel(self.adc_address2, 0xD8)
        return self.getadcreading(self.adc_address2, 0xD8)
    
    def readCSeven14bit(self):
        self.setDivisor(4)
        self.changechannel(self.adc_address2, 0xD4)
        return self.getadcreading(self.adc_address2, 0xD4)
    
    def readCSeven14bit(self):
        self.setDivisor(1)
        self.changechannel(self.adc_address2, 0xD0)
        return self.getadcreading(self.adc_address2, 0xD0)
    
    def readCEight18bit(self):
        self.setDivisor(128)
        self.changechannel(self.adc_address2, 0xFD)
        return self.getadcreading(self.adc_address2, 0xFD)
    
    def readCEight16bit(self):
        self.setDivisor(32)
        self.changechannel(self.adc_address2, 0xF9)
        return self.getadcreading(self.adc_address2, 0xF9)
    
    def readCEight14bit(self):
        self.setDivisor(8)
        self.changechannel(self.adc_address2, 0xF5)
        return self.getadcreading(self.adc_address2, 0xF5)
    
    def readCEight12bit(self):
        self.setDivisor(2)
        self.changechannel(self.adc_address2, 0xF1)
        return self.getadcreading(self.adc_address2, 0xF1)
        
        
    