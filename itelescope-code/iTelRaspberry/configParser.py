from xml.dom.minidom import parse
from angles import Angle
import datetime
import numpy as np

class configParser(object):
    
    def __init__(self,fileName):
        self.fileName = fileName
        self.parse()
        
    def parse(self):
        self.dom = parse(self.fileName)
    
    def printXML(self):
        print >> self.configFile, self.dom.toprettyxml("    ")
        
    def setGeneric(self,node,attribute,value):
        self.parse()
        theNode = self.dom.getElementsByTagName(node)[0]
        theNode.attributes[attribute] = value
        self.configFile = open(self.fileName, "w")
        self.printXML()
        self.configFile.close()
        
    def getGeneric(self,node,attribute):
        self.parse()
        theNode = self.dom.getElementsByTagName(node)[0]
        value = theNode.getAttributeNode(attribute).nodeValue
        return value
        
    def getLatLon(self):
        uLat = self.getGeneric('location', 'latitude')
        Lat = Angle(r=float(uLat))
        uLon = self.getGeneric('location', 'longitude')
        Lon = Angle(r=float(uLon))
        return [Lat,Lon]
    
    def setLatLon(self,location):
        Lat = location[0]
        Lon = location[1]
        self.setGeneric('location', 'latitude', str(Lat.r))
        self.setGeneric('location', 'longitude', str(Lon.r))
        
    def setTime(self,timeType,theTime):
        self.setTimeType(timeType)
        self.setGeneric('time', 'string', theTime.strftime('%Y-%m-%d-%H-%M-%S'))
        
    def setTimeType(self,timeType):
        self.setGeneric('time', 'type', timeType)
        
    def getTime(self):
        timeString = self.getGeneric('time', 'string')
        theTime = datetime.datetime.strptime(timeString,'%Y-%m-%d-%H-%M-%S')
        return theTime
    
    def getTimeType(self):
        timeType  = self.getGeneric('time', 'type')
        return timeType
        
    def getAllConfigData(self):
        attributeDictionary = {}
        attributeDictionary['location'] = ['latitude','longitude','altitude']
        attributeDictionary['time'] = ['string','type']
        
        data=[]
        
        for key in attributeDictionary.keys():
            for attribute in attributeDictionary[key]:
                data.append("%s:%s:%s" % (key, attribute, self.getGeneric(key, attribute)))
        
        return data
        
class calibrationParser(configParser):
    
    def getAzimuthCalibration(self):
        AzCalUp = self.getCoefficientsNode("azimuth", "up")
        AzCalDn = self.getCoefficientsNode("azimuth", "down")
        return [AzCalUp,AzCalDn]
        
    def getAltitudeCalibration(self):
        AltCalUp = self.getCoefficientsNode("altitude", "up")
        AltCalDn = self.getCoefficientsNode("altitude", "down")
        return [AltCalUp,AltCalDn]
        
    
    def getCoefficientsNode(self,axis,direction):
        axisNode = self.dom.getElementsByTagName(axis)[0]
        directionNode = axisNode.getElementsByTagName(direction)[0]
        theNode = directionNode.getElementsByTagName("coefficients")[0]
        value = theNode.getAttributeNode("c").nodeValue
        #theCoeffs = [double(x) for x in value.split(',')]
        theCoeffs = map( float, value.split(',') )
        return theCoeffs
    
    def setAzAltCorrection(self,rotationMatrix):
        for i in range(9):
            self.setGeneric("correctionMatrix", ("e%i" % i), str(rotationMatrix.item(i)))
        
    def getAzAltCorrection(self):
        rMat = np.matrix(np.identity(3))
        for i in range(9):
            rMat.itemset(i,float(self.getGeneric("correctionMatrix", ("e%i" % i))))
            
        return rMat
        
        
        
    