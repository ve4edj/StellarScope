#!/usr/bin/env python
"""
@file    stellariumConnect.py
@author  Simon Box
@date    13/02/2013

"""

import socket, sys, angles, struct, time, select

class stellariumConnect(object):
    def __init__(self,host,port):
        self.serverAddress=(host,port)
        
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.serverAddress)
        self.sock.settimeout(600)#Throws a timeout exception if connections are idle for 10 minutes
        self.sock.listen(1)#set the socket to listen, now it's a server!
        self.connected = False
        
    def handshakeStellarium(self):
        try:
            while True:
                # Wait for a connection
                self.connection, self.clientAddress = self.sock.accept() 
                if self.connection != None:
                    self.connected = True
                    break
        except Exception:
            print "Failed handshake with Stellarium: %s" % (Exception.message)
            
        
    def sendStellariumCoords(self,Ra,Dec):
        [RaInt,DecInt] = self.angleToStellarium(Ra, Dec)
        data = struct.pack("3iIii", 24, 0, time.time(), RaInt, DecInt, 0)##//TODO time reported here does not include the offset (if any). This may not be an issue but you should check. 
        self.sendStellariumData(data)
    
    def receiveStellariumCoords(self,timeout):
        incomingData = self.receiveStellariumData(timeout)
        if incomingData != None:
            data = struct.unpack("3iIi", incomingData)
            [Ra,Dec] = self.stellariumToAngle(data[3], data[4])
            return [Ra,Dec]
        else:
            return [False,False]
    
    def receiveStellariumData(self,timeout):
        try:
            incomingData = None
            ready = select.select([self.connection], [], [], timeout)
            if ready[0]:
                incomingData = self.connection.recv(640)
            return incomingData
        except Exception, e:
            print "failed to receive light data from Stellarium: %s" % e
            
    def sendStellariumData(self,data):
        try:
            for i in range(10):##Stellarium likes to recieve the coordinates 10 times.
                self.connection.send(data)
        except Exception, e:
            print "failed to send data to Stellarium: %s" % e
            
    def angleToStellarium(self,Ra,Dec):
        return [int(Ra.h*(2147483648/12.0)), int(Dec.d*(1073741824/90.0))]
    
    def stellariumToAngle(self,RaInt,DecInt):
        Ra = angles.Angle(h=(RaInt*12.0/2147483648))
        Dec = angles.Angle(d=(DecInt*90.0/1073741824))
        return [Ra, Dec]
        
    #def stellariumTime(self,mtime):
    #    time_s = math.floor(mtime / 1000000)
    #    stellTime = datetime.datetime(localtime(time_s))
    #    return stellTime
        
    def closeConnection(self):
        self.connection.close()
        self.sock.close()
        sys.stdout.flush()
    
        