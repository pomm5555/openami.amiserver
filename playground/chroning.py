# -*- coding: utf-8 -*-

from Packets.Packet import Packet
from threading import Thread
import time


class chrontest(Thread):
    def __init__ (self):
        Thread.__init__(self)

    def run(self):
        while 1:
            print "hallo"
            time.sleep(1)


if __name__ == "__main__":
    p = Packet("from@jabber.org", "to@jabber.org")
    p.addString("min", "1")
    p.addString("hour", "*")
    p.addString("day of month", "*")
    p.addString("month", "*")
    p.addString("day of week", "*")
    p.addString("path", "*")
    print p


    #c = chrontest()
    #c.start()
