import time, datetime, stellariumConnect 
from angles import Angle
from subprocess import call


class uInterface(object):
    def splash(self):
        print "************************************************"
        print "**                iTELESCOPE v2.0             **"
        print "**                                            **"
        print "** by Simon Box - http://simonbox.info        **"
        print "** UTC: %s                   **" % datetime.datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')
        print "************************************************\n"
                
    def mainMenu(self,theClient,cfgData):
        if theClient.connected:
            theClient.sendTime()
            theClient.sendFullConfig(cfgData)
        
        while(True):
            print "** Main Menu:\n"
            print "** 1. Set Location"
            print "** 2. Set Time"
            print "** 3. Connect to Stellarium"
            print "** 4. Read Coordinates"
            print "** 5. Calibrate"
            print "** 6. Quit\n"
            print "** Enter menu number:"
            
            uInput = raw_input()
            
            if uInput == "1":
                self.locationMenu(cfgData)
                theClient.sendFullConfig(cfgData)
                #break
            elif uInput == "2":
                self.setTimeMenu(cfgData)
                theClient.sendTime()
                theClient.sendFullConfig(cfgData)
                #break
            elif uInput == "3":
                self.stellariumConnectMenu(theClient)
                #break
            elif uInput == "4":
                self.readCoordinatesMenu(theClient)
                #break
            elif uInput == "5":
                self.calibrationMenu(theClient)
                #break
            elif uInput == "6":
                print "Ending all processes, please wait...."
                break
            else:
                print "Error %s is not a valid menu option please try again." % uInput
                
    def locationMenu(self,cfgData):
        
        while(True):
            print "** Current Location:\n"
            [Lat,Lon] = cfgData.getLatLon()
            Lat.ounit = "degrees"
            Lon.ounit = "degrees"
            print "** Latitude:%s" % Lat
            print "** Longitude:%s\n" % Lon
            
            print "** Location Menu:\n"
            print "** 1. Accept current location"
            print "** 2. Set new location"
            print "** 3. Return to Main Menu\n"
            
            print "** Enter menu number:"
            
            uInput = raw_input()
            
            if uInput == "1":
                #self.mainMenu()
                break
            elif uInput == "2":
                Latitude = self.setAngleMenu("Latitude")
                print "Latitude set to: %s" % Latitude
                Longitude = self.setAngleMenu("Longitude")
                print "Longitude set to: %s" % Longitude
                cfgData.setLatLon([Latitude,Longitude])
            elif uInput == "3":
                #self.mainMenu()
                break
            else:
                print "Error %s is not a valid menu option please try again." % uInput
                
    def setAngleMenu(self,angleName):
        while(True):
            print "** Enter %s\n" % angleName
            print "** Use one of the following formats:"
            print "** Option 1: Degrees \"D\" e.g. 15.1275"
            print "** Option 2: Degrees:Minutes \"DD:M\" e.g. 15:7.65"
            print "** Option 3: Degrees:Minutes:Seconds \"DD:MM:SS\" e.g. 15:07:39"
            print "** %s:" % angleName
            
            uInput = raw_input()

            try:
                theAngle = Angle(uInput)
                return theAngle
                break
            except ValueError as e:
                print "There was an error in the angle value that you entered: %s" % e.message
                
    def setTimeMenu(self,cfgData):
        while(True):
            
            print "**Current system time: %s\n" % datetime.datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')
            print "**Time Menu:\n"
            print "** 1. Use system time"
            print "** 2. Use custom time "
            print "** 3. Return to Main Menu\n"
            
            print "** Enter menu number:"
            
            uInput = raw_input()
            
            if uInput == "1":
                cfgData.setTime("system",datetime.datetime.utcnow())
                break
            elif uInput == "2":
                theTime = self.inputTime()
                cfgData.setTime("custom",theTime)
                break
            elif uInput == "3":
                #self.mainMenu()
                break
            else:
                print "Error %s is not a valid menu option please try again." % uInput
                
    def inputTime(self):
        while(True):
            print "Enter the time using the format:"
            print "\"YYYY-mm-dd-HH-MM-SS\" e.g. 2013-03-31-16-04-21\n"
            print "Enter time:"
            
            uInput = raw_input()
            
            try:
                theTime = datetime.datetime.strptime(uInput,'%Y-%m-%d-%H-%M-%S')
                return theTime
                break
            except TypeError as e:
                print "There was an error in the time value that you entered: %s" % e.message
            except ValueError as e:
                print "There was an error in the time value that you entered: %s" % e.message
    
    
    def stellariumConnectMenu(self,theClient):
        host = "localhost"
        port = 10001
        while(True):
            print "** Telescope server ready"
            print "** The host is: %s" % host
            print "** The port is: %u\n" % port
            
            print "** Telescope server Menu"
            print "** IMPORTANT! You must start this server *before* attempting to connect via Stellarium"
            print "** 1. Start server"
            print "** 2. Change host and port"
            print "** 3. Return to Main Menu"
            
            uInput = raw_input()
            
            if uInput=="1":
                print "Telescope server started."
                print "Connect from within stellarium using host=%s and port=%u" % (host, port)
                stelCon = stellariumConnect.stellariumConnect(host,port)
                stelCon.handshakeStellarium()
                theClient.stellariumMode(stelCon)
                break
            elif uInput=="2":
                host = self.setAddresHost()
                port = self.setAddressPort()
            elif uInput=="3":
                break
            else:
                print "Error %s is not a valid menu option please try again." % uInput

    def setAddresHost(self):
        print "Please enter the server host name e.g. \"localhost\" or 127.0.0.1"
        uInput = raw_input()
        return uInput
    
    def setAddressPort(self):
        while(True):
            print "Please enter the server port number e.g. 10001"
            uInput = raw_input()
            try:
                uNumber = int(uInput)
                break
            except:
                print "Oops! %s is not an integer please try again" % uInput
            
        return uNumber       
                   
    def readCoordinatesMenu(self, theClient):      
        #call("clear") #commented as does not work under windows ans functionality non-essential
        print "** Current coordinates of telescope orientation:\n"
        theClient.evaluationMode()
        
        #print "** Azimuth: %s " % "0000"
        #print "** Altitude: %s\n " % "0000"
        #print "** Right Ascension: %s " % "0000"
        #print "** Declination: %s " % "0000"
            
    def calibrationMenu(self,theClient):
        host = "localhost"
        port = 10001
        while(True):
            print "** iTelescope calibration instructions:\n"
            print "** Calibration uses Stellarium, Connect from within Stellarium (after starting the server below)."
            print "** Point the telescope at a known star (e.g. Polaris) then select that star in Stellarium"
            print "** Issue the \"go to\" command from Stellarium (ctrl + <Telescope Number>)\n"
            
            print "** Telescope server ready"
            print "** The host is: %s" % host
            print "** The port is: %u\n" % port
            
            print "** 1. Start Stellarium server"
            print "** 2. Change host and port"
            print "** 3. I have aligned the telescope myself thanks (reset corrections to zero)."
            print "** 4. Return to Main Menu"
            
            uInput = raw_input()
            
            if uInput=="1":
                print "Telescope server started."
                print "Connect from within stellarium using host=%s and port=%u" % (host, port)
                stelCon = stellariumConnect.stellariumConnect(host,port)
                stelCon.handshakeStellarium()
                theClient.calibrationMode(stelCon)
                #stelCon.closeConnection()
                #stelCon = stellariumConnect.stellariumConnect(host,port)
                #stelCon.handshakeStellarium()
                #theClient.stellariumMode(stelCon)
                break
            elif uInput=="2":
                host = self.setAddresHost()
                port = self.setAddressPort()
            elif uInput=="3":
                theClient.calibrationReset()
            elif uInput=="4":
                break
            else:
                print "Error %s is not a valid menu option please try again." % uInput
            
        
        

                
        
            
    
