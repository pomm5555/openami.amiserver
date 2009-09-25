#!/usr/bin/python
from EventEngine import EventEngine
from supay import Daemon
import time, sys, os
from amiConfig import Config


'''
Executing amiServer needs supay, a lib for daemonizing python script
use:
    easy_install supay
to install...

'''

abs_path = os.path.abspath(".")
name='amiServerd'
pid_dir=abs_path+'/run'
stdin=abs_path+'/logs'
stdout=abs_path+'/logs'
stderr=abs_path+'/logs'


def run():
    daemon = Daemon(name, pid_dir, stdin, stdout, stderr)
    daemon.start()

    try:
        start_event_engine()
    except Exception, e:
        print "[ERROR] ",
        print e

    stat()
    print "removing "+pid_dir+"/"+name+".pid"
    os.remove(pid_dir+"/"+name+".pid")
    stop()


def stop():
    daemon = Daemon(name, pid_dir, stdin, stdout, stderr)
    daemon.stop()


def stat():
    daemon = Daemon(name, pid_dir, stdin, stdout, stderr)
    daemon.status()


def start_event_engine():
    print "starting event engine..."
    e = EventEngine()


def display_help():
    print "Usage:\npython amiServer.py <argument>"
    print "arguments:\n\tstart\tstarts the daemon\n\tstop\t stops the daemon\n\tstat\t displays status information\n\tproc\t start amiService as regular process"

if __name__ == "__main__":
    if sys.argv.__len__() == 2:
        if sys.argv[1].__eq__("start"):
            run()
        elif sys.argv[1].__eq__("stop"):
            stop()
        elif sys.argv[1].__eq__("stat"):
            stat()
        elif sys.argv[1].__eq__("proc"):
            start_event_engine()
        else:
            display_help()
    else:
        display_help()
