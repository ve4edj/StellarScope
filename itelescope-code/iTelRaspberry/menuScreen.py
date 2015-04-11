from screenPrinter import screenPrinter

class menuScreen(object):
    def __init__(self,sysTme,cfgParse):
        self.outScreen = 0
        self.sysTme = sysTme
        self.cfgParse = cfgParse
        
    def printLatLong(self):
        [Lat,Lon] = self.cfgParse.getLatLon()
        Lat.ounit = "degrees"
        Lon.ounit = "degrees"
        screenPrinter().printToScreen("Lat: %s\nLon: %s" % (Lat,Lon))

    def printTime(self):
        screenPrinter().printToScreen("UTC: %s\n%s"%(self.sysTme.getDateStr(),self.sysTme.getTimeStr()))
        
    def printSwitcher(self):
        if(self.outScreen==0):
            self.printLatLong()
            self.outScreen = 1
        elif(self.outScreen==1):
            self.printTime()
            self.outScreen = 0
        