from uInterface import uInterface
from blueClient import blueClient
from configParser import configParser

if __name__ == '__main__':
    uInterface().splash()
    theClient = blueClient()
    cfgData = configParser("config.xml")
    uInterface().mainMenu(theClient,cfgData)
    