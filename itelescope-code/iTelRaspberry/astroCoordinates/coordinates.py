'''
Created on 9 Apr 2013

@author: sb4p07
'''
import angles, sidereal

class coordinates(object):


    def __init__(self,sysTime,config):
        self.sysTime = sysTime
        [self.Lat,self.Lon] = config.getLatLon()
        self.LatLon = sidereal.LatLon(self.Lat.r,self.Lon.r)
        
    def getRaDec(self,Az,Alt):
        
        AltAz = sidereal.AltAz(Alt.r,Az.r)

        GST = sidereal.SiderealTime.fromDatetime(self.sysTime.getTime())
        LST = GST.lst(self.Lon.r)
    
        RaDec = AltAz.raDec(LST, self.LatLon)
    
        Ra = angles.Angle(r=RaDec.ra)
        Dec = angles.Angle(r=RaDec.dec)
        
        return [Ra,Dec]
        
    def getAzAlt(self,Ra,Dec):
        
        RaDec = sidereal.RADec(Ra.r,Dec.r)
        
        AltAz = RaDec.altAz(RaDec.hourAngle(self.sysTime.getTime(), self.Lon.r), self.Lat.r)
        
        Az = angles.Angle(r=AltAz.az)
        Alt = angles.Angle(r=AltAz.alt)
        
        return [Az,Alt]
        
        
        
        
        