import angles, sidereal

class coordinates(object):

    def __init__(self,sysTime):
        self.sysTime = sysTime
        [self.Lat,self.Lon] = [angles.Angle(d=49.8997541), angles.Angle(d=-97.1374937)]
        self.LatLon = sidereal.LatLon(self.Lat.r,self.Lon.r)
        
    def getRaDec(self,Az,Alt):
        
        AltAz = sidereal.AltAz(Alt.r,Az.r)

        GST = sidereal.SiderealTime.fromDatetime(self.sysTime)
        LST = GST.lst(self.Lon.r)
    
        RaDec = AltAz.raDec(LST, self.LatLon)
    
        Ra = angles.Angle(r=RaDec.ra)
        Dec = angles.Angle(r=RaDec.dec)
        
        return [Ra,Dec]
        
    def getAzAlt(self,Ra,Dec):
        
        RaDec = sidereal.RADec(Ra.r,Dec.r)
        
        AltAz = RaDec.altAz(RaDec.hourAngle(self.sysTime, self.Lon.r), self.Lat.r)
        
        Az = angles.Angle(r=AltAz.az)
        Alt = angles.Angle(r=AltAz.alt)
        
        return [Az,Alt]