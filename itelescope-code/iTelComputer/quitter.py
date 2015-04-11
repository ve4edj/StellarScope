'''
Created on 20 Apr 2013

@author: simon
'''
import threading

class quitter(threading.Thread):
    def __init__(self,message):
        threading.Thread.__init__(self)
        self.message = message
        self.alive = True
    
    def run(self):
        print "%s is running, enter \'q\' to quit\n" % self.message
        self.alive = True
        while self.alive:
            char = raw_input()
            if char == "q" or "Q":
                self.alive = False
                break
            
    def kill(self):
        self.alive = False
            