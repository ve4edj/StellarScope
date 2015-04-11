'''
Created on 25 Jun 2013

@author: sb4p07
'''
#from analogRead import analogRead
from voltageCalibration import voltageCalPair,voltageCalibration
from astroCoordinates.coordinates import coordinates

class reportTester(object):
    def __init__(self,cfgParser,calParser,sysTime):
        #self.analogR = analogRead()
        [AzCalUp,AzCalDn] = calParser.getAzimuthCalibration()
        [AltCalUp,AltCalDn] = calParser.getAltitudeCalibration()
        
        self.AzimuthCal = voltageCalPair(voltageCalibration(AzCalUp),voltageCalibration(AzCalDn))
        self.AltitudeCal = voltageCalPair(voltageCalibration(AltCalUp),voltageCalibration(AltCalDn))
        
        self.astro = coordinates(sysTime,cfgParser)
        
    def getRaDec(self,v1,v2):
        return self.astro.getRaDec(self.getAz(v1),self.getAlt(v2))
    
    def getAz(self,vIn):
        voltage = vIn
        #voltage = 1.5
        Azimuth = self.AzimuthCal.voltageToAngle(voltage)
        return Azimuth
        
    def getAlt(self,vIn):
        voltage = vIn
        #voltage = 1.5
        Altitude = self.AltitudeCal.voltageToAngle(voltage)
        return Altitude
        