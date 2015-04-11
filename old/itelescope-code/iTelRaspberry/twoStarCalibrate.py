'''
Created on 27 Jun 2013

@author: sb4p07
'''
import numpy as np
import math
from twoStarCorrection import twoStarCorrection

class twoStarCalibrate(twoStarCorrection):
    def __init__(self,log):
        self.reset()
        self.logger = log
        

    def reset(self):
        self.stars=[]
        self.starCount = 0
        self.testPass = True       
           
    def addStar(self,telStar,stelStar):
        self.stars.append(star(telStar,stelStar))
        self.starCount = self.starCount + 1
        
    def getRotationMatrix(self):
        if(self.starCount==1):
            return self.oneStarRotationMatrix()
        elif(self.starCount==2):
            return self.twoStarRotationMatrix()
        else:
            self.logger.error("Rotation matrix calculation failed. The identity was used instead")
            return np.matrix(np.identity(3))
            
        
    def oneStarRotationMatrix(self):
        if(self.starCount<1):
            raise IndexError("There are no loaded stars so cannot calculate Matrix")
        
        theStar = self.stars[0]
        dAz = self.plusMinus180(theStar.sAz-theStar.tAz)
        #dAlt = self.plusMinus180(theStar.sAlt-theStar.tAlt)
        qAz = self.__buildQuaternion(dAz, [0,0,1])
        #qAlt = self.__buildQuaternion(dAlt, [0,1,0])
        
        #q = self.__quaternionProduct(qAz, qAlt)
        R = self.__quaternionToMatrix(qAz)
        if self.testMatrix(R):
            return R
        else:
            self.testPass = False
            return self.getIdentityMatrix()
        
    
    def twoStarRotationMatrix(self):
        if(self.starCount<2):
            raise IndexError("There not enough loaded stars for a two star calibration")
        
        st1 = self.stars[0]
        st2 = self.stars[1]
        
        telMat = self.__twoStarDiffernceMatrix([st1.tAz,st1.tAlt], [st2.tAz,st2.tAlt])
        stelMat = self.__twoStarDiffernceMatrix([st1.sAz,st1.sAlt], [st2.sAz,st2.sAlt])
        
        R = np.linalg.solve(stelMat.T,telMat.T)
        if self.testMatrix(R):
            return R
        else:
            self.testPass = False
            return self.oneStarRotationMatrix()
    
    def getIdentityMatrix(self):
        return np.matrix(np.identity(3))
    
    def testMatrix(self,R):
        if np.isnan(R.sum()) or np.isinf(R.sum()):
            return False
        else:
            return True    
    
    def __twoStarDiffernceMatrix(self,star1,star2):
        c1 = self.AzAltToVec(star1[0], star1[1])
        c2 = self.AzAltToVec(star2[0], star2[1])
        c3 = np.cross(c1, c2)
        c3 = c3/np.linalg.norm(c3)
        
        M = np.matrix([c1,c2,c3])
        M = M.T
        return M
        
        pass
    
    
    def __buildQuaternion(self,angle,axis):
        sinAngle = math.sin(angle/2)
        quaternion = np.array([math.cos(angle/2), sinAngle*axis[0], sinAngle*axis[1], sinAngle*axis[2]])
        return quaternion
    
    def __quaternionToMatrix(self,quaternion):
        s=quaternion[0];
        vx=quaternion[1];
        vy=quaternion[2];
        vz=quaternion[3];
        
        i1j1=1-2*math.pow(vy,2)-2*math.pow(vz,2);
        i1j2=2*vx*vy-2*s*vz;
        i1j3=2*vx*vz+2*s*vy;
        i2j1=2*vx*vy+2*s*vz;
        i2j2=1-2*math.pow(vx,2)-2*math.pow(vz,2);
        i2j3=2*vy*vz-2*s*vx;
        i3j1=2*vx*vz-2*s*vy;
        i3j2=2*vy*vz+2*s*vx;
        i3j3=1-2*math.pow(vx,2)-2*math.pow(vy,2);
        
        R = np.matrix([[i1j1, i1j2, i1j3], [i2j1, i2j2, i2j3],[i3j1, i3j2, i3j3]])
        return R
    
    def __quaternionProduct(self,q,r):
        s1 = q[0]
        v1 = np.array([q[1],q[2],q[3]])
        
        s2 = r[0]
        v2 = np.array([r[1],r[2],r[3]])
        
        sO = s1*s2 - np.dot(v1,v2)
        vO = s1*v2 + s2*v1 + np.cross(v1, v2)
        qO = np.array([sO,vO[0],vO[1],vO[2]])
        qO =qO/np.linalg.norm(qO)
        return qO

class star(object):
    def __init__(self,telCoords,stelCoords):
        self.tAz = telCoords[0].r
        self.tAlt = telCoords[1].r
        
        self.sAz = stelCoords[0].r
        self.sAlt = stelCoords[1].r       
        
    
        
        
    
