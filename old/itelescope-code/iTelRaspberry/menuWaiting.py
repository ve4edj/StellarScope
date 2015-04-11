'''
Created on 3 Jul 2013

@author: simon
'''
import threading, time
from screenPrinter import screenPrinter

class menuWaiting(threading.Thread):
    def __init__(self,cfg,sysTme):
        threading.Thread.__init__(self)
        #self.logger = log
        self.cfgParser = cfg
        self.sysTme = sysTme;
        self.alive = True
        
    def run(self):
        self.alive = True
        try:
            tStart = time.time()
            oneSet = False
            twoSet = False
            while self.alive:
                if time.time() - tStart < 3:
                    if not oneSet:
                        [Lat,Lon] = self.cfgParser.getLatLon()
                        Lat.ounit = "degrees"
                        Lon.ounit = "degrees"
                        screenPrinter().printToScreen("Lat: %s\nLon: %s" % (Lat,Lon))
                        oneSet = True;
                elif time.time() - tStart < 6:
                    if not twoSet:
                        screenPrinter().printToScreen("UTC:%s\n%s" % (self.sysTme.getDateStr(),self.sysTme.getTimeStr()))
                        #screenPrinter().printToScreen("a Message")
                        twoSet=True;
                else:
                    tStart = time.time()
                    oneSet = False
                    twoSet = False
                    
        except Exception as e:
            screenPrinter().printToScreen("Read config fail\ncheck log")
            #self.logger.error(e.message)
            
        
    def endThread(self):
        self.alive = False
        
