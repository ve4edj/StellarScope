import stellariumConnect, datetime, math
from angles import Angle 
from twoStarCalibrate import twoStarCalibrate
import numpy as np
from configParser import calibrationParser

stel1 = [Angle(r=1.6666*math.pi),Angle(r=math.pi/4)]
stel2 = [Angle(r=-math.pi/1.1),Angle(r=math.pi/52)]

tel1 = [Angle(r= -2.084132566391469),Angle(r= 0.785398163397448)]
tel2 = [Angle(r= 2.390466410049688),Angle(r= 0.060415243338265)]

TSC = twoStarCalibrate()
TSC.addStar(tel1, stel1)
TSC.addStar(tel2, stel2)

R = TSC.twoStarRotationMatrix()
R1 = TSC.oneStarRotaionMatrix()

TSC.addRotationMatrix(R)

[Az2,Alt2] = TSC.correct(-3.036725575684632, 0.300000000000000)

calP = calibrationParser("instrumentCalibration.xml")
calP.setAzAltCorrection(R)

Rp = calP.getAzAltCorrection()
print Rp
print R
print [Az2,Alt2]




sCon = stellariumConnect.stellariumConnect('localhost',10001)
sCon.handshakeStellarium()

while True:
    [Ra, Dec] = sCon.receiveStellariumCoords(10)
    if Ra != False:
        Ra.ounits = "hours"
        Dec.ounits = "degrees"
        print "%s / %s" % (Ra,Dec)
        sCon.sendStellariumCoords(Ra, Dec)
    
    