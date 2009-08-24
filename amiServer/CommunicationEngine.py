# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="markus"
__date__ ="$Aug 19, 2009 6:26:15 PM$"

import xmpp
import sys

class CommunicationEngine:

    def __init__(self, root, jid, pwd):

        self.root = root
        self.jid=xmpp.protocol.JID(jid)
        self.client = xmpp.Client(self.jid.getDomain(), debug=[])

        # connect client
        if self.client.connect() == "":
            print "not connected"
            sys.exit(0)

        # authenticate client
        if self.client.auth(self.jid.getNode(), pwd) == None:
            print "authentication failed"
            sys.exit(0)

        # register message handler
        self.client.RegisterHandler('message', self.messageCB)

        # set presencehandler and presence
        self.client.RegisterHandler('presence', self.presenceCB)
        self.client.sendInitPresence()

        print "Communicationengine is online, or should be... #TODO" #TODO

        # go to eventLoop
        self.goOn(self.client)



    def messageCB(self, conn, msg):
        content = str(msg.getBody())
        sender = str(msg.getFrom())
        print "Sender: " + sender +" Content: " + content

        # prints parts of the address, here must happen the message deserialisation! TODO
        # flag packets comming from messages received while unpresent
        #print content[0:1]
        #print content[1:]


        print "*"

        if content.__eq__("get"):
            self.send(self.root.returnTree(0), sender)

        elif content.__eq__("xml"):
            self.send(self.root.toXml(), sender)

        elif content.__eq__("help"):
            self.send("enter\nhelp to print this message\nxml to print xml representation\nget to print message overview", sender)

        elif content[0:1].__eq__("/"):
            #try:
            result = self.root.getByAddress(content[1:]).use()
            self.send(result, sender)
            print result
            #except:
            #    self.send("*"+content+" is not a valid address.", sender)

        elif content.split("\n")[0].__eq__("<?xml version=\"1.0\" ?>"):
            self.packetHandler(content, sender)


        else:
            self.send("0", sender)


    def presenceCB(self, conn,msg):
        print str(msg)
        prs_type=msg.getType()
        who=msg.getFrom()
        if prs_type == "subscribe":
            conn.send(xmpp.Presence(to=who, typ = 'subscribed'))
            conn.send(xmpp.Presence(to=who, typ = 'subscribe'))

    def stepOn(self, conn):
        try:
            conn.Process(1)
        except KeyboardInterrupt:
            return 0
        return 1

    def goOn(self, conn):
        while self.stepOn(conn):
            pass

    def send(self, msg, sender):
        self.client.send(xmpp.protocol.Message(sender,msg))


    def contentHandler(self, message, sender):
        print message

