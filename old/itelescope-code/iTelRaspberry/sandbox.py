from setSysTime import setSysTime
import datetime, math
import numpy as np
from configParser import configParser,calibrationParser
from voltageCalibration import voltageCalibration,voltageCalPair
from twoStarCorrection import twoStarCorrection

'''

setTme = setSysTime()
setTme.setSystemTime("1979-02-14-12-12-12")

R = np.matrix(np.identity(3))

TSC = twoStarCorrection(R)

Alt = math.pi/4
Az = 1.25*math.pi

Vec = TSC.AzAltToVec(Az, Alt)
[cAz,cAlt] = TSC.VecToAzAlt(Vec)

print [cAz,cAlt]


setTme = setSysTime()
ds = setTme.getDateStr()
ts = setTme.getTimeStr()
#from blueServer import blueServer
import astroCoordinates.coordinates
import angles
#from reportCoordinates import reportCoordinates
from reportTester import reportTester

calPs = calibrationParser("instrumentCalibration.xml")
cfgPs = configParser("config.xml")
sysTme = setSysTime()

repTest = reportTester(cfgPs,calPs,sysTme);
Az = repTest.getAz(1.4)
Alt = repTest.getAlt(0.75)
Alt.ounit = "degrees"
print Alt


#reporter = reportCoordinates(cfgPs,calPs,sysTme)
#[ra,dec] = reporter.getRaDec()


thing = calPs.getAzimuthCalibration()
thing2 = calPs.getAltitudeCalibration()
'''

coefsUP = [5.0347,-24.076,-90.606,346.7]
vcUP = voltageCalibration(coefsUP)

coefsDN = [-27.176,83.623,-207.86,389.99]
vcDN = voltageCalibration(coefsDN)

vcp = voltageCalPair(vcUP,vcDN)

a = vcp.voltageToAngle(1.47689)
b = vcp.voltageToAngle(1.47689)
c = vcp.voltageToAngle(0.566)
d = vcp.voltageToAngle(0.31)
e = vcp.voltageToAngle(0.31)


timePiece = setSysTime()
cfgPs = configParser("config.xml")
coord = astroCoordinates.coordinates.coordinates(timePiece,cfgPs)

'''
Ra= angles.Angle('0h44m15s')
Dec = angles.Angle('-17d54m51s')

[Az, Alt] = coord.getAzAlt(Ra, Dec)
Az.ounit = "degrees"
Alt.ounit = "degrees" 
print "%s / %s" % (Az,Alt)

'''
Az= angles.Angle('199d40m14s')
Alt = angles.Angle('19d34m53s')

[Ra, Dec] = coord.getRaDec(Az, Alt)
Ra.ounit = "hours"
Dec.ounit = "degrees" 
print "%s / %s" % (Ra,Dec)



#cfgPs = configParser("config.xml")
#theServer = blueServer()
#theServer.reportingMode(cfgPs)
#ssT = setSysTime()

#ssT.setSystemTime("1997-02-14-12-00-00")
#cfgPs = configParser("config.xml")
#ssT.setTimeFromConfig(cfgPs)


#print ssT.getTime()
