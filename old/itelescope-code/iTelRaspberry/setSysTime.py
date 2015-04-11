import datetime
import subprocess

class setSysTime(object):
    
    def __init__(self):
        self.type = "system"#Can also be set to "custom"
        self.offset = datetime.timedelta(0)

    def getTime(self):
        if self.type == "system":
            return datetime.datetime.utcnow()
        else:
            return datetime.datetime.utcnow() - self.offset
        
    def getDateStr(self):
        dt = self.getTime()
        return(dt.strftime('%d/%m/%Y'))
    
    def getTimeStr(self):
        dt = self.getTime()
        return(dt.strftime('%H:%M:%S'))
        
    def setSystemTime(self,tString):
        sysTime = datetime.datetime.strptime(tString,'%Y-%m-%d-%H-%M-%S')
        #command = 'sudo date -s \"%s\"' % sysTime.strftime('%m/%d/%Y %H:%M:%S')#Note this command will work on raspbian wheezy but not non-Debian based Linux installs 
        subprocess.check_call(["date","-u","-s", sysTime.strftime('%m/%d/%Y %H:%M:%S')])
        self.type = "system"
        
    
    def setCustomTime(self,tObj):
        self.offset = datetime.datetime.utcnow() - tObj
        self.type = "custom"
        
    def setTimeFromConfig(self,cfgData):
        if cfgData.getTimeType() == "custom":
            self.setCustomTime(cfgData.getTime())
            
            