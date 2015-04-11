from bluetooth import *
import datetime, angles, threading, quitter, time

class blueClient(object):
    def __init__(self):
        self.uuid = "17a84160-9b83-11e2-9e96-0800200c9a66"
        self.search()
        self.connected = False
        self.connect()
    
    def getUUID(self):
        return self.uuid
    
    def setUUID(self,inUUID):
        self.uuid = inUUID
        self.search
        
    def search(self):
        print "Searching for iTelRaspberry services with uuid=%s" % self.uuid
        self.serviceMatches = find_service( uuid = self.uuid, address = None )
        
    def connect(self):
        if len(self.serviceMatches) == 0:
            print "WARNING: No iTelRaspberry services found"
        else:
            firstMatch = self.serviceMatches[0]
            port = firstMatch["port"]
            name = firstMatch["name"]
            host = firstMatch["host"]
            print "connecting to \"%s\" on %s" % (name, host)
            
            try:
                # Create the client socket
                self.clientSock = BluetoothSocket( RFCOMM )
                self.clientSock.connect((host, port))
                
                ##HandShake
                try:
                    while True:
                        self.clientSock.send("iTelRaspberry I presume")
                        data = self.clientSock.recv(1024)
                        if len(data) == 0: 
                            pass
                        elif data=="iTelComputer I presume":
                            print "Connected to iTelRaspberryServer"
                            self.connected = True
                            break            
                except IOError as e:
                    print "Handshake failed, %s" % e.message
            except IOError as e:
                    print "Connection failed %s" % e.message
                    
    def sendFullConfig(self,cfgParser):
        data = cfgParser.getAllConfigData()
        for chunk in data:
            try:
                self.clientSock.send("sendingConfig")
                answer = self.clientSock.recv(1024)
                if answer == "receivingConfig":
                    self.clientSock.send(chunk)
                    completion = self.clientSock.recv(1024)
                    if completion != "configReceived":
                        print "Error: the iTelRaspberry server did not confirm receipt of the config data"
                else:
                    print "Error: the iTelRaspberry server did not want to receive the config data"
            except IOError as e:
                print "Sending config failed, check connection %s" % e.message
                
    def sendTime(self):
            try:
                self.clientSock.send("sendingTime")
                answer = self.clientSock.recv(1024)
                if answer == "receivingTime":
                    self.clientSock.send(datetime.datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S'))
                    completion = self.clientSock.recv(1024)
                    if completion != "timeReceived":
                        print "Error: the iTelRaspberry server did not confirm receipt of the time data"
                else:
                    print "Error: the iTelRaspberry server did not want to receive the time data"
            except IOError as e:
                print "Sending time failed, check connection %s" % e.message
    """            
    def sendTarget(self,target):
            try:
                self.clientSock.send("goTo")
                answer = self.clientSock.recv(1024)
                if answer == "receivingTarget":
                    self.clientSock.send(target)
                else:
                    print "Error: the iTelRaspberry server did not want to receive the target star"
            except IOError as e:
                print "Sending time failed, check connection %s" % e.message
    """
        
    def evaluationMode(self):
        theQuitCall = quitter.quitter("The position evaluator")
        theQuitCall.start()
        try:
            self.clientSock.send("report")
            while theQuitCall.alive:
                reading = self.clientSock.recv(1024)
                radecS  = reading.split(":")
                Ra = angles.Angle(r=float(radecS[0]))
                Dec = angles.Angle(r=float(radecS[1]))
                Ra.ounit = "degrees"
                Dec.ounit = "degrees"
                print "Ra :%s" % Ra
                print "Dec:%s" % Dec
                self.clientSock.send("1")
                
            self.clientSock.send("0")
            completion = self.clientSock.recv(1024)
            if completion != "reportingComplete":
                print "Error: the iTelRaspberry server did not confirm completion of reporting mode"       
        except IOError as e:
                print "evaluation mode failed, check connection %s" % e.message
    
    
    def calibrationReset(self):
        self.clientSock.send("resetCalibration")
        answer = self.clientSock.recv(1024)
        if(answer == "calibrationReset"):
            print "iTelescope calibration corrections have been zeroed."
        else:
            print "Error: iTelescope did not confirm that calibration was reset."
                
    def calibrationMode(self,stelCom):
        calibrationMode(self.clientSock,stelCom)
    
    def stellariumMode(self,stelCom):
        stellariumMode(self.clientSock,stelCom)
        """
        theQuitCall = quitter.quitter("The Stellarium server")
        theQuitCall.start()
        try:
            stelReceiver = stellariumReceive(stelCom)
            stelReceiver.start()
            self.clientSock.send("report")
            while theQuitCall.alive:
                reading = self.clientSock.recv(1024)
                radecS  = reading.split(":")
                Ra = angles.Angle(r=float(radecS[0]))
                Dec = angles.Angle(r=float(radecS[1]))
                stelCom.sendStellariumCoords(Ra,Dec)
                
                if(stelReceiver.hasTarget):
                    self.clientSock.send("0")
                    self.sendTarget(stelReceiver.getTargetString())
                    stelReceiver.targetReceived()
                    self.clientSock.send("report")
                else:
                    self.clientSock.send("1")
            
            if(stelReceiver.hasTarget):
                self.sendTarget(stelReceiver.getTarget())
                stelReceiver.targetReceived()
                
            self.clientSock.send("0")
            stelReceiver.endThread()              
            stelCom.closeConnection()
                
        except IOError as e:
            self.clientSock.send("0")
            stelReceiver.endThread() 
            self.stelCom.closeConnection()
            print "Sending time failed, check connection %s" % e.message
        #if self.connected:
        #    stelConnector = stellariumMode(self.clientSock,stelCom)
        #else:
        #    stelConnector = fakeStellariumMode(stelCom)#DEBUGGING ONLY
        #    
        #theQuitCall = quitter.quitter("The Stellarium server")
        #stelConnector.start()
        #theQuitCall.run()     
        #stelConnector.endThisThread = True
        """    
                
                    
                
    def closeConnection(self):
        self.clientSock.close()
        self.connected = False
"""        
class evaluationMode(threading.Thread):
    def __init__(self,clientSock):
        self.clientSock = clientSock
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            self.clientSock.send("report")
            i=0
            while (True):
                reading = self.clientSock.recv(1024)
                print reading
                i+=1
                if i < 1000:
                    self.clientSock.send("1")
                else:
                    self.clientSock.send("0")
        except IOError as e:
                print "Sending time failed, check connection %s" % e.message
"""                
class stellariumMode(object):
    def __init__(self,clientSock,stelCom):
        self.clientSock = clientSock
        self.stelCom = stelCom
        self.theQuitCall = quitter.quitter("The Stellarium server")
        self.theQuitCall.start()
        try:
            self.stelReceiver = stellariumReceive(stelCom)
            self.stelReceiver.start()
            
            while self.theQuitCall.alive:
                self.reportingLoop()
                self.clientSock.send("0")
                completion = self.clientSock.recv(1024)
                if completion != "reportingComplete":
                    print "Error: the iTelRaspberry server did not confirm completion of reporting mode"
                
                if self.stelReceiver.hasTarget:
                    self.sendTarget()
                else:
                    break
            
            self.stelReceiver.endThread()              
            self.stelCom.closeConnection() 
            
        except IOError as e:
            self.clientSock.send("0")
            self.stelReceiver.endThread() 
            self.stelCom.closeConnection()
            print "Sending time failed, check connection %s" % e.message
    
    def reportingLoop(self):
        self.clientSock.send("report")
        while self.theQuitCall.alive:
                reading = self.clientSock.recv(1024)
                radecS  = reading.split(":")
                Ra = angles.Angle(r=float(radecS[0]))
                Dec = angles.Angle(r=float(radecS[1]))
                self.stelCom.sendStellariumCoords(Ra,Dec)
                
                if(self.stelReceiver.hasTarget):
                    break
                else:
                    self.clientSock.send("1")      
    
    def sendTarget(self):
        target = self.stelReceiver.getTargetString()
        try:
            self.clientSock.send("goTo")
            answer = self.clientSock.recv(1024)
            if answer == "receivingTarget":
                self.clientSock.send(target)
                self.stelReceiver.targetReceived()
                completion = self.clientSock.recv(1024)
                if completion != "targetReceived":
                    print "Error: the iTelRaspberry server did not confirm receipt of the target star"
            else:
                print "Error: the iTelRaspberry server did not want to receive the target star"
        except IOError as e:
            print "Sending time failed, check connection %s" % e.message
        

class calibrationMode(stellariumMode):
    def __init__(self,clientSock,stelCom):
        self.nuberOfStars = 0
        super(calibrationMode,self).__init__(clientSock,stelCom)
        self.sendCalibrationComplete()
        
    def sendTarget(self):
        target = self.stelReceiver.getTargetString()
        try:
            self.clientSock.send("calibration")
            answer = self.clientSock.recv(1024)
            if answer == "receivingTarget":
                self.clientSock.send(target)
                self.stelReceiver.targetReceived()
                completion = self.clientSock.recv(1024)
                if completion != "targetReceived":
                    print "Error: the iTelRaspberry server did not confirm receipt of the target star"
                self.nuberOfStars += 1
                self.messagePicker()
                
            else:
                print "Error: the iTelRaspberry server did not want to receive the target star"
        except IOError as e:
            print "Sending time failed, check connection %s" % e.message
            
    def messagePicker(self):
        if self.nuberOfStars == 1:
            print "iTelescope has calibrated using the one star method. To stick with this enter 'q'.\nOr to use the more accurate two star method, pick another star."
        elif self.nuberOfStars == 2:
            print "iTelescope has calibrated using the two star method.\nTo repeat the calibration procedure just pick another star,\nor to use the calibrated telescope enter 'q' and go into Stellarium Mode from the main menu."
            self.nuberOfStars =0
            self.sendCalibrationComplete()
            
    def sendCalibrationComplete(self):
        try:
            self.clientSock.send("endCalibration")
            answer = self.clientSock.recv(1024)
            if answer == "calibrationPass":
                pass
            elif answer == "calibrationErrors":
                print "Warning: iTelescope found errors in the calibration data. Telescope may be fully or partially un-calibrated."
            else:
                print "Error: the iTelRaspberry server did not confirm termination of calibration mode"
        except IOError as e:
            print "Sending end calibration signal failed %s" % e.message
            
    
    
    
"""            
class fakeStellariumMode(threading.Thread):##DEBUGGING Only
    def __init__(self,stelCom):
        self.target = None
        self.stelCom = stelCom
        threading.Thread.__init__(self)
        self.endThisThread = False
        
    def run(self):
        #//TODO add threading to this bit to receive GOTO commands
        try:
            i=0
            stelReceiver = stellariumReceive(self.stelCom)
            stelReceiver.start()
            reading = "0:0"
            while (True):  
                radecS  = reading.split(":")
                Ra = angles.Angle(r=float(radecS[0]))
                Dec = angles.Angle(r=float(radecS[1]))
                self.stelCom.sendStellariumCoords(Ra,Dec)
                if self.target != None:
                    reading = "%02f:%02f" % (self.target[0].r,self.target[1].r)
                    #print reading
                if self.endThisThread:
                    stelReceiver.endThisThread = True
                    break
                time.sleep(0.1)
                
        except IOError as e:
                print "Sending time failed, check connection %s" % e.message
"""                
class stellariumReceive(threading.Thread):
    def __init__(self,stelCom):
        self.stelCom = stelCom
        #self.stelMod = stelMod
        threading.Thread.__init__(self)
        self.alive = True
        self.target = None
        self.hasTarget = False
        
    def run(self):
        self.alive = True
        try:
            while self.alive:
                targ = self.stelCom.receiveStellariumCoords(5)
                if targ[0]!= False:
                    self.newTarget(targ)
                    
                
        except IOError as e:
            print "Error in receiving coordinates from Stellarium: %s" % e.message
                    
        
    def newTarget(self,targ):
        self.target = targ
        self.hasTarget = True
        
    def getTargetString(self):
        tString = "%02f:%02f" % (self.target[0].r,self.target[1].r)
        return tString
        
    def targetReceived(self):
        self.hasTarget = False   
        
    def endThread(self):
        self.alive = False   
    