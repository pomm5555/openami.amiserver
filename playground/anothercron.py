from datetime import datetime, timedelta
import time
from threading import Thread

# Some utility classes / functions first
class AllMatch(set):
    """Universal set - match everything"""
    def __contains__(self, item): return True

allMatch = AllMatch()

def conv_to_set(obj):  # Allow single integer to be provided
    if isinstance(obj, (int,long)):
        return set([obj])  # Single item
    if not isinstance(obj, set):
        obj = set(obj)
    return obj

# The actual Event class
class Event(object):
    def __init__(self, action, min=allMatch, hour=allMatch,
                       day=allMatch, month=allMatch, dow=allMatch,
                       args=(), kwargs={}):
        self.mins = conv_to_set(min)
        self.hours= conv_to_set(hour)
        self.days = conv_to_set(day)
        self.months = conv_to_set(month)
        self.dow = conv_to_set(dow)
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def matchtime(self, t):
        """Return True if this event should trigger at the specified datetime"""
        return ((t.minute     in self.mins) and
                (t.hour       in self.hours) and
                (t.day        in self.days) and
                (t.month      in self.months) and
                (t.weekday()  in self.dow))

    def check(self, t):
        if self.matchtime(t):
            self.action(*self.args, **self.kwargs)

class CronTab(Thread):
    def __init__(self, *events):
        Thread.__init__(self)
        self.events = events

    def run(self):
        t=datetime(*datetime.now().timetuple()[:5])
        while 1:
            print "entering endless while"
            for e in self.events:
                e.check(t)

            t += timedelta(minutes=1)
            while datetime.now() < t:
                print datetime.now().__str__()+" < "+t.__str__()
                print "sleeping "+str((t - datetime.now()).seconds)
                #print "why: (>"+t.__str__()+"< - >"+ datetime.now().__str__()+"<).seconds)"
                time.sleep((t - datetime.now()).seconds)



def test():
    print "test"


c = CronTab(
  Event(test, range(0,60))
)

c.start()
print "thread started"