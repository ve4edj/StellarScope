'''
Created on 30 Jun 2013

@author: simon
'''
import numpy as np
import math
from angles import Angle

class twoStarCorrection(object):
    def __init__(self,rotationMatrix):
        self.addRotationMatrix(rotationMatrix)
        
    def addRotationMatrix(self,rotationMatrix):
        self.rotationMatrix = rotationMatrix
        
    def correct(self,Az,Alt):
        tVec = self.AzAltToVec(Az.r, Alt.r)
        tV = np.matrix([tVec])
        dVec = self.rotationMatrix*tV.T
        [rAz, rAlt] = self.VecToAzAlt(dVec)
        aAz = Angle(r=rAz)
        aAlt = Angle(r=rAlt)
        return [aAz,aAlt]       
        
    def plusMinus180(self,theAngle):
        while (theAngle <= -math.pi): 
            theAngle = theAngle + 2*math.pi

        while (theAngle > math.pi): 
            theAngle = theAngle - 2*math.pi
        
        return theAngle
        
    def VecToAzAlt(self,vecIn):
        vecIn = vecIn/np.linalg.norm(vecIn)
        Alt = math.asin(vecIn[2])
        pAz = math.atan(vecIn[1]/vecIn[0])
        Az = 0   
        #This only works due to the +- 180 stuff?
        if (vecIn[0]>=0):
            Az = pAz
        elif (vecIn[0]<0):
            Az = math.pi+pAz
            
        Az = self.plusMinus180(Az);
        return [Az,Alt]
    
    
    def AzAltToVec(self,Az,Alt):
        z = self.plusMinus180(Az)
        t = self.plusMinus180(Alt)    
        v = np.array([math.cos(t)*math.cos(z),math.cos(t)*math.sin(z),math.sin(t)])
        return v