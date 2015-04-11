from analogRead import analogRead
from voltageCalibration import voltageCalPair,voltageCalibration
from astroCoordinates.coordinates import coordinates
from twoStarCorrection import twoStarCorrection

class reportCoordinates(object):
    def __init__(self,cfgParser,calParser,sysTime):
        self.analogR = analogRead()
        [AzCalUp,AzCalDn] = calParser.getAzimuthCalibration()
        [AltCalUp,AltCalDn] = calParser.getAltitudeCalibration()
        self.correction = twoStarCorrection(calParser.getAzAltCorrection())
        
        self.AzimuthCal = voltageCalPair(voltageCalibration(AzCalUp),voltageCalibration(AzCalDn))
        self.AltitudeCal = voltageCalPair(voltageCalibration(AltCalUp),voltageCalibration(AltCalDn))
        
        self.astro = coordinates(sysTime,cfgParser)
        
    def getRaDec(self):
        [Az,Alt] = self.getAzAlt()
        return self.astro.getRaDec(Az,Alt)
    
    def getTAz(self):
        voltage = self.analogR.readChannelSeven()
        #voltage = 1.5
        Azimuth = self.AzimuthCal.voltageToAngle(voltage)
        return Azimuth
        
    def getTAlt(self):
        voltage = self.analogR.readChannelEight()
        #voltage = 1.5
        Altitude = self.AltitudeCal.voltageToAngle(voltage)
        return Altitude
    
    def getAzAlt(self):
        return self.correction.correct(self.getTAz(), self.getTAlt())
        
    def convertToAzAlt(self,Ra,Dec):
        [Az,Alt] = self.astro.getAzAlt(Ra, Dec)
        return [Az,Alt]
        