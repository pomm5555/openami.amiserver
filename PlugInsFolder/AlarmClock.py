import os, datetime, threading, sched, time, Address
from AmiTree import *
from PlugIn import PlugIn
from amiConfig import Config
from EventEngine import EventEngine


class AlarmClock(PlugIn):

    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"
        
        global active, ringTime, wday, scheduler, alarmEvent
        wday = []
        alarmEvent = None
        #Read from Config
        active = AlarmClock.strToBool(Config.get("AlarmClock", "active"))
        ringTime = Config.get("AlarmClock", "time")
        wday.append(AlarmClock.strToBool(Config.get("AlarmClock", "monday")))
        wday.append(AlarmClock.strToBool(Config.get("AlarmClock", "tuesday")))
        wday.append(AlarmClock.strToBool(Config.get("AlarmClock", "wednesday")))
        wday.append(AlarmClock.strToBool(Config.get("AlarmClock", "thursday")))
        wday.append(AlarmClock.strToBool(Config.get("AlarmClock", "friday")))
        wday.append(AlarmClock.strToBool(Config.get("AlarmClock", "saturday")))
        wday.append(AlarmClock.strToBool(Config.get("AlarmClock", "sunday")))
        
        scheduler = sched.scheduler(time.time, time.sleep)
        AlarmClock.schedAlarm()

        #Build Tree
        #plugin itself
        self.content = Container("plugin", token, "Alarm Clock")
        #ON/OFF
        self.content.addChild(SwitchContainer("cmd", "TurnOnAlarm", "Turn On Alarm", self.toogleAlarm, on=Config.jid + "/AlarmClock/TurnOnAlarm?string=True", off=Config.jid + "/AlarmClock/TurnOnAlarm?string=False", checked=active))
        #Time
        self.content.addChild(TimefieldContainer("cmd", "Time", "Set Time", self.setTime, target=Config.jid + "/AlarmClock/Time", value=ringTime))
        #Days
        self.content.addChild(CheckBoxContainer("cmd", "Monday", "Alarm on Monday", self.checkMonday, toogle=Config.jid + "/AlarmClock/Monday", checked=wday[0]))
        self.content.addChild(CheckBoxContainer("cmd", "Tuesday", "Alarm on Tuesday", self.checkTuesday, toogle=Config.jid + "/AlarmClock/Tuesday", checked=wday[1]))
        self.content.addChild(CheckBoxContainer("cmd", "Wednesday", "Alarm on Wednesday", self.checkWednesday, toogle=Config.jid + "/AlarmClock/Wednesday", checked=wday[2]))
        self.content.addChild(CheckBoxContainer("cmd", "Thursday", "Alarm on Thursday", self.checkThursday, toogle=Config.jid + "/AlarmClock/Thursday", checked=wday[3]))
        self.content.addChild(CheckBoxContainer("cmd", "Friday", "Alarm on Friday", self.checkFriday, toogle=Config.jid + "/AlarmClock/Friday", checked=wday[4]))
        self.content.addChild(CheckBoxContainer("cmd", "Saturday", "Alarm on Saturday", self.checkSaturday, toogle=Config.jid + "/AlarmClock/Saturday", checked=wday[5]))
        self.content.addChild(CheckBoxContainer("cmd", "Sunday", "Alarm on Sunday", self.checkSunday, toogle=Config.jid + "/AlarmClock/Sunday", checked=wday[6]))
        #Save
        self.content.addContainer("cmd", "save", "save alarm", self.save)
        
    def execAlarm():
        global alarmEvent
        alarmEvent = None
        print "ALARM ALARM"

        addr = Address(Config.get("AlarmClock", "exec"))
        print addr.__str__()
        print EventEngine.root.getByAddress(addr.__str__()).use()
        
        time.sleep(1)
        print AlarmClock.schedAlarm()
    execAlarm = staticmethod(execAlarm)
        
    def save(self, var=""):
        Config.setOption("AlarmClock", "active", str(active))
        Config.setOption("AlarmClock", "time", str(ringTime))
        Config.setOption("AlarmClock", "monday", str(wday[0]))
        Config.setOption("AlarmClock", "tuesday", str(wday[1]))
        Config.setOption("AlarmClock", "wednesday", str(wday[2]))
        Config.setOption("AlarmClock", "thursday", str(wday[3]))
        Config.setOption("AlarmClock", "friday", str(wday[4]))
        Config.setOption("AlarmClock", "saturday", str(wday[5]))
        Config.setOption("AlarmClock", "sunday", str(wday[6]))
        return AlarmClock.schedAlarm()
    
    def toogleAlarm(self, swStr=""):
        global active
        active = AlarmClock.strToBool(swStr)
        self.setChecked(active)
        return ""
        
    def setTime(self, var="00:00"):
        global ringTime
        ringTime = str(var)
        self.setValue(ringTime)
        print "SET_TIME " + ringTime
    
    def checkMonday(self, cbStr):
        global wday
        wday[0] = AlarmClock.strToBool(cbStr)
        self.setChecked(wday[0])
        return ""
        
    def checkTuesday(self, cbStr):
        global wday
        wday[1] = AlarmClock.strToBool(cbStr)
        self.setChecked(wday[1])
        return ""
        
    def checkWednesday(self, cbStr):
        global wday
        wday[2] = AlarmClock.strToBool(cbStr)
        self.setChecked(wday[2])
        return ""
        
    def checkThursday(self, cbStr):
        global wday
        wday[3] = AlarmClock.strToBool(cbStr)
        self.setChecked(wday[3])
        return ""
    
    def checkFriday(self, cbStr):
        global wday
        wday[4] = AlarmClock.strToBool(cbStr)
        self.setChecked(wday[4])
        return ""
        
    def checkSaturday(self, cbStr):
        global wday
        wday[5] = AlarmClock.strToBool(cbStr)
        self.setChecked(wday[5])
        return ""
        
    def checkSunday(self, cbStr):
        global wday
        wday[6] = AlarmClock.strToBool(cbStr)
        self.setChecked(wday[6])
        return ""

    def strToBool(st):
        if(st=="True"):
            return True
        return False
    strToBool = staticmethod(strToBool)
    
    def schedAlarm():
        global wday, ringTime, alarmEvent, active, scheduler
        
        if(alarmEvent):
            scheduler.cancel(alarmEvent)
            alarmEvent = None
        
        try:
            if(active):
                #calc Time for Ring event
                now = datetime.datetime.today()
                parsedTime = datetime.datetime.strptime(ringTime, "%H:%M").time()
                waitdays = 0
                if(wday[now.weekday()] == False or now.time() > parsedTime) :
                    waitdays = 1
                    weday=now.weekday()
                    while(waitdays<=7):
                        if((weday + waitdays) > 6):
                            weday = weday -7
                        if(wday[weday + waitdays]):
                            break
                        waitdays = waitdays + 1
                
                if(waitdays==8):
                    return "Fail to set Alarm - Please enable a weekday"
                
                nextRing = now + datetime.timedelta(days=waitdays)
                nextRing = datetime.datetime.combine(nextRing.date(), parsedTime)
                
                td = nextRing-now
                sec = td.days*86400 + td.seconds + td.microseconds/1000000
                
                #setAlarm
                alarmEvent = scheduler.enter(sec, 3, AlarmClock.execAlarm, ())
                threading.Thread(target=scheduler.run).start()
                return "Successful - Next alarm in " + str(td.days) + " Days and " + str(td.seconds) + " seconds"
            else:
                return "Alarm disabled"
        except:
            return "Fail to set Alarm - Please check timefield"
        
    schedAlarm = staticmethod(schedAlarm)
    
class TimefieldContainer(Container):

    def __init__(self, type, token, information="empty", use=None, logging=False, target=None, value=""):
        Container.__init__(self, type, token, information, use, logging)
        self.target = target
        self.value = value

    def toJqHtmlElement(self):
        if self.visible:
            content = '<li><input type="text" name="'+self.token+'" placeholder="'+self.token+'" id="sole_name" onBlur="if(/^([0-1][0-9]|[2][0-3]):([0-5][0-9])$/.test(this.value) == false) alert(\'incorrect timeformat - HH:MM\'); else $.get(\''+self.target+'?string=\'+$(this).val());" value="'+self.value+'"/></li>'
            return content
        else:
            return ""
        
    def setValue(self, value):
        self.value = value       

