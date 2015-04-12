from coordinates import coordinates
from twoStarCorrection import twoStarCorrection

class reportCoordinates(object):
    def __init__(self,sysTime):
        self.astro = coordinates(sysTime)
        self.correction = twoStarCorrection(calParser.getAzAltCorrection())
        
    def getRaDec(self, yaw, pitch):
        [Az,Alt] = self.getAzAlt(yaw, pitch)
        return self.astro.getRaDec(Az,Alt)
    
    def getAzAlt(self, yaw, pitch):
        return self.correction.correct(yaw, pitch)
        
    def convertToAzAlt(self,Ra,Dec):
        [Az,Alt] = self.astro.getAzAlt(Ra, Dec)
        return [Az,Alt]
        