from blueServer import blueServer
from configParser import configParser,calibrationParser
from screenPrinter import screenPrinter
from unConnected import unConnected
import logging


if __name__ == '__main__':
    ## Set up logging
    logger = logging.getLogger('iTelescope')
    hdlr = logging.FileHandler('iTelescope.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    #logger.setLevel(logging.WARNING)
    ######
    
    ## name config files
    cfgP = configParser("config.xml")
    calP = calibrationParser("instrumentCalibration.xml")
    ######
    while True:
        try:   
            ## Start the unConnected thread
            basic = unConnected(cfgP,calP,logger)
            basic.start()
            
            ## Start the bluetooth server and listen        
            theServer = blueServer(logger)
            theServer.listenForConnection()
            
            basic.endThread()## terminate the unConnected thread on connection
            ######
            
            ## On connection exchange config files and enter config mode
            theServer.configMode(cfgP,calP)
            ######
            theServer.closeConnection()
            screenPrinter().printToScreen("iTelescope is \n restarting...")
            logger.warning("iTelescope restarted due to running through")
            
        except Exception as e:
            
            screenPrinter().printToScreen("iTelescope is \n restarting...")
            logger.error("iTelescope restarted due to error: %s" % e.message)
            logger.exception("details:")