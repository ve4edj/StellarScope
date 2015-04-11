'''
Created on 25 Jun 2013

@author: simon
'''
import threading, time
from screenPrinter import screenPrinter
from setSysTime import setSysTime
from reportCoordinates import reportCoordinates

class unConnected(threading.Thread):
    def __init__(self,cfg,cal,log):
        threading.Thread.__init__(self)
        self.logger = log
        self.cfgParser = cfg
        self.calParser = cal
        self.sysTme = setSysTime();
        self.reporter = reportCoordinates(self.cfgParser,self.calParser,self.sysTme)
        self.alive = True
        
    def run(self):
        self.alive = True
        try:
            tStart = time.time()
            while self.alive:
                if time.time() - tStart < 3:
                    [Az,Alt] = self.reporter.getAzAlt()
                    Az.ounit = "degrees"
                    Alt.ounit = "degrees"
                    screenPrinter().printToScreen("Az : %s\nAlt: %s" % (Az,Alt))
                elif time.time() - tStart < 6:
                    [Ra,Dec] = self.reporter.getRaDec()
                    Ra.ounit = "hours"
                    Dec.ounit = "degrees"
                    screenPrinter().printToScreen("Ra : %s\nDec: %s" % (Ra,Dec))
                else:
                    tStart = time.time()
                    
        except Exception as e:
            screenPrinter().printToScreen("Read coord fail\ncheck log")
            self.logger.error(e.message)
            
        
    def endThread(self):
        self.alive = False
        