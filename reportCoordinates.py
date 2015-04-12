from coordinates import coordinates

class reportCoordinates(object):
    def __init__(self,sysTime):
        self.astro = coordinates(sysTime)
        
    def getRaDec(self, yaw, pitch):
        [Az,Alt] = [yaw, pitch]
        return self.astro.getRaDec(Az,Alt)
    
    def convertToAzAlt(self,Ra,Dec):
        [Az,Alt] = self.astro.getAzAlt(Ra, Dec)
        return [Az,Alt]
        