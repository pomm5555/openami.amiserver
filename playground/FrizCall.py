#!/usr/bin/env python
import socket

def simpleHandler(d):
    """a very simple handler for incoming calls, prints to stdout"""
    if d[1] == 'RING':
        print 'Incoming call from: %s to: %s' % (d[3], d[4])
    elif d[1] == 'CALL':
        print 'Outgoing call from: %s to: %s via: %s' % (d[4], d[5], d[6])
    elif d[1] == 'DISCONNECT':
        print 'Call ended!'


class IncomingCallMonitor:
    """monitors incoming calls on any Fritz!Box Phone device, you
    need to enable the call monitor by dialing #96*5* on a telephone"""
    def __init__(self, handler=simpleHandler):
        self.handler = handler

    def start(self, host='fritz.box', port=1012):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        while 1:
            line = s.recv(1024)
            if not line:
                break
            self.handler(line.strip().split(';'))
        s.close()


if __name__ == '__main__':
    import os

    try:
        monitor.start()
    except KeyboardInterrupt:
        pass