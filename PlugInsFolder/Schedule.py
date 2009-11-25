# -*- coding: utf-8 -*-

from AmiTree import *
from PlugIn import PlugIn
from amiConfig import Config
from EventEngine import EventEngine
from Address import Address
import time, socket

class Schedule(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        # set plugins "hardware" architecture for system dependencies
        self.content = "all"

        # create plugin itself
        self.content = ThreadContainer("plugin", token, "This hopefully will be a Scheduler  Plugin")

        self.content.setDo(self.sched)

        # start thread
        self.content.start()


    def sched(self):

        d = Config.getSection("Scheduler")

	if not d == []:
            #print d
            while True:

                sleeptime = None
                for elem in d:
                    rhythm = eval(elem[1].split("|")[1])
                    # when has the thread to wake up next time for specific value?
                    tmp = rhythm - round(time.time()) % rhythm
                    if not sleeptime:
                        sleeptime = tmp
                    if sleeptime > tmp:
                        sleeptime = tmp

                time.sleep(sleeptime)

                execute = []
                for elem in d:
                    rhythm = eval(elem[1].split("|")[1])
                    if rhythm - round(time.time()) % rhythm == rhythm:
                        execute.append(elem)

                for elem in execute:
                    addr = Address(elem[1].split("|")[0])
                    print addr.__str__()
                    print EventEngine.root.getByAddress(addr.__str__()).use()
