'''
Created on 2 Jun 2013

@author: simon
'''
from angles import Angle
import math


class voltageCalPair:
    
    def __init__(self,upCalibration,downCalibration):
        self.upCalibration = upCalibration
        self.downCalibration = downCalibration
        self.lastPosition = Angle(d=0)
        self.ascending = True
        self.voltageRecord = [0,0]
        self.buffer = 0.0002
        
    def voltageToAngle(self,volts):
        #low pass filter
        #volts = 0.8*volts + 0.2*self.lastVoltage
        
        if volts != self.voltageRecord[1]:
            if volts > (self.voltageRecord[1] + self.buffer) and self.voltageRecord[1] > (self.voltageRecord[0] + self.buffer):
                self.ascending = True
            elif volts < (self.voltageRecord[1] - self.buffer) and self.voltageRecord[1] < (self.voltageRecord[0] - self.buffer):
                self.ascending = False
                   
            
            if self.ascending:
                position = (self.upCalibration.voltageToAngle(volts))
            else:
                position = (self.downCalibration.voltageToAngle(volts))
            
            self.voltageRecord[0] = self.voltageRecord[1]
            self.voltageRecord[1] = volts
        else:
            position = self.lastPosition
        
        
        self.lastPosition = position
        return position
            
            



class voltageCalibration:
    
    def __init__(self,coeficients):
        self.coeficients = coeficients
        
    def voltageToAngle(self,volts):
        power=0
        degrees = 0
        for c in reversed(self.coeficients):
            degrees += math.pow(volts, power)*c
            power+=1
            
        return(Angle(d=degrees))
            
        
        
