from bluetooth import *
from screenPrinter import screenPrinter
from setSysTime import setSysTime
from reportCoordinates import reportCoordinates
from angles import Angle 
from twoStarCalibrate import twoStarCalibrate
from menuScreen import menuScreen
import time

class blueServer(object):
    def __init__(self,log):
        self.logger=log
        self.calibration = twoStarCalibrate(log)
        self.serverSock=BluetoothSocket( RFCOMM )
        self.serverSock.bind(("",PORT_ANY))
        self.serverSock._sock.settimeout(600)#Throws a timeout exception if connections are idle for 10 minutes
        self.serverSock.listen(1)
        
        self.port = self.serverSock.getsockname()[1]
        
        self.uuid = "17a84160-9b83-11e2-9e96-0800200c9a66"
        self.advertise()
        self.connected = False
        
    def advertise(self):  
        advertise_service( self.serverSock, "iTelRaspberryServer", service_id = self.uuid, service_classes = [ self.uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ], protocols = [ OBEX_UUID ] )
                   
    def getUUID(self):
        return self.uuid
    
    def setUUID(self,inUUID):
        self.uuid = inUUID
        self.advertise()
        
    def listenForConnection(self):
        screenPrinter().printToScreen("Wait for client\n Channel %d" % self.port)
        try:
            self.clientSock, self.clientInfo = self.serverSock.accept()
            ##HandShake
            try:
                while True:
                    data = self.clientSock.recv(1024)
                    if len(data) == 0: 
                        pass
                    elif data=="iTelRaspberry I presume":
                        self.clientSock.send("iTelComputer I presume")
                        screenPrinter().printToScreen("Connected to\n iTelComputer")
                        #screenPrinter().printToScreen(self.clientInfo)
                        self.connected = True 
                        break           
            except IOError as e:
                screenPrinter().printToScreen("Handshake failed\ncheck log")
                self.logger.error("Handshake failed: %s" % e.message)
        
        except IOError as e:
            screenPrinter().printToScreen("Connection fail\ncheck log")
            self.logger.error("Connection fail: %s" % e.message)
            
    def configMode(self,cfgParser,calParser):
        if self.connected:
            setTme = setSysTime()
            menuScn = menuScreen(setTme,cfgParser)
            try:
                while True:
                    menuScn.printSwitcher()
                    data = self.clientSock.recv(1024)
                    if len(data) == 0:
                        pass
                    elif data == "sendingTime":
                        self.receiveTime(setTme)
                        #screenPrinter().printToScreen("UTC Time: %s" % setTme.getTime())
                    
                    elif data == "sendingConfig":
                        self.receiveConfig(cfgParser,setTme)
                        #[Lat,Lon] = self.cfgParser.getLatLon()
                        #Lat.ounit = "degrees"
                        #Lon.ounit = "degrees"
                        #screenPrinter().printToScreen("Lat: %s\nLon: %s" % (Lat,Lon))
                        
                    elif data == "goTo":
                        [Ra,Dec] = self.receiveTarget()
                        Ra.ounit = "degrees"
                        Dec.ounit = "degrees"
                        screenPrinter().printToScreen("TR : %s\nTD: %s" % (Ra,Dec))
                    
                    elif data == "calibration":
                        self.calibration.reset()
                        self.calibrationMode(cfgParser, calParser, setTme)
                        
                    elif data == "endCalibration":
                        if self.calibration.testPass:
                            self.clientSock.send("calibrationPass")
                        else:
                            self.clientSock.send("calibrationErrors")
                            self.logger.warning("NaNs or infs were found in the rotation matrix after calibration")
                        
                        self.calibration.reset()
                        
                    elif data == "resetCalibration":
                        calParser.setAzAltCorrection(self.calibration.getIdentityMatrix())
                        self.calibration.reset()
                        self.clientSock.send("calibrationReset")      
                        
                    elif data == "report":
                        self.reportingMode(cfgParser,calParser,setTme)
                    elif data == "disconnect":
                        pass#TODO this is not implemented yet...
                    else:
                        screenPrinter().printToScreen("Unknown command\n %s" % data)
                    
            except IOError as e:
                screenPrinter().printToScreen("Config fail\ncheck log")
                self.logger.error("Config fail: %s" % e.message)
        else:
            screenPrinter().printToScreen("Config fail\n No connection")
            
    def receiveConfig(self,cfgParser,setTme):
        self.clientSock.send("receivingConfig")
        data = self.clientSock.recv(1024)
        cfgData = str.split(data,':')
        cfgParser.setGeneric(cfgData[0],cfgData[1],cfgData[2])
        setTme.setTimeFromConfig(cfgParser)
        self.clientSock.send("configReceived")
        
    def receiveTime(self,setTme):
        self.clientSock.send("receivingTime")
        data = self.clientSock.recv(1024)
        try:
            setTme.setSystemTime(data)
        except Exception as e:
            screenPrinter().printToScreen("Time set fail\ncheck log")
            self.logger.error("Error setting rPi time: %s" % e.message)
        self.clientSock.send("timeReceived")
        
    def receiveTarget(self):
        self.clientSock.send("receivingTarget")
        data = self.clientSock.recv(1024)
        self.clientSock.send("targetReceived")
        radecS  = data.split(":")
        Ra = Angle(r=float(radecS[0]))
        Dec = Angle(r=float(radecS[1]))
        return [Ra,Dec]
        
                        
    def reportingMode(self,cfgParser,calParser,sysTime):
        reporter = reportCoordinates(cfgParser,calParser,sysTime)
        while(True):
            [Ra,Dec] = reporter.getRaDec()
            sRaDe = "%02f:%02f" % (Ra.r,Dec.r)
            self.clientSock.send(sRaDe)
            Ra.ounit = "hours"
            Dec.ounit = "degrees"
            screenPrinter().printToScreen("Ra : %s\nDec: %s" % (Ra,Dec))
            data = self.clientSock.recv(1024)
            if data == "1":
                pass
            else:
                self.clientSock.send("reportingComplete")
                break
                
    def calibrationMode(self,cfgParser,calParser,sysTime):
        [Ra,Dec] = self.receiveTarget()
        reporter = reportCoordinates(cfgParser,calParser,sysTime)
        tAz = reporter.getTAz()
        tAlt = reporter.getTAlt()
        [sAz,sAlt] = reporter.convertToAzAlt(Ra, Dec)
        self.calibration.addStar([tAz,tAlt], [sAz,sAlt])
        calParser.setAzAltCorrection(self.calibration.getRotationMatrix())
        
                    
                
    def closeConnection(self):
        self.serverSock.close()
        self.connected = False