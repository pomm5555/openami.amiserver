# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="markus"
__date__ ="$Aug 19, 2009 6:26:15 PM$"

import xmpp
import sys
from Packets.Packet import Packet

class CommunicationEngine:

    def __init__(self, root, jid, pwd, host, port, ressource):

        self.root = root
        self.jid=xmpp.protocol.JID(jid)
        self.host = host
        self.port = port
        self.client = xmpp.Client(self.jid.getDomain(), debug=[])

        # connect client
        if self.client.connect((host, port)) == "":
            print "not connected"
            sys.exit(0)

        # authenticate client
        if self.client.auth(self.jid.getNode(), pwd, ressource) == None:
            print "authentication failed"
            sys.exit(0)

        # register message handler
        self.client.RegisterHandler('message', self.messageHandler)

        # set presencehandler and presence
        self.client.RegisterHandler('presence', self.presenceHandler)
        self.client.sendInitPresence()

        # register disconnect handler
        self.client.RegisterDisconnectHandler(self.disconnectHandler)


        #init roster
        self.processRoster()
        
        print "Communicationengine is online, or should be... #TODO" #TODO

        # go to eventLoop
        self.goOn(self.client)



    def messageHandler(self, conn, msg):
        print unicode(dir(msg))
        print unicode(msg.getFrom()).split("/")[0]
        print self.jid
        content = unicode(msg.getBody())
        sender = unicode(msg.getFrom())
        print "Sender: " + sender + " Content: " + content

        print "*"


        if content.__eq__("show"):
            self.send(self.root.returnTree(0), sender)

        elif content.__eq__("xml"):
            self.send(self.root.toXml(), sender)

        elif content.__eq__("list"):
            #result = ""
            #for elem self.root.getAddressList():
            #    result += elem+"\n"
            self.send(self.root.getAddressList().__str__(), sender)

        elif content.__eq__("help"):
            self.send("enter\nhelp to print this message\nxml to print xml representation\nget to print message overview", sender)

        elif content[0:1].__eq__("/"):
            #try:
            result = self.root.getByAddress(content[1:]).use()
            self.send(result, sender)
            print result
            #except:
            #    self.send("[ERROR] "+content+" is not a valid address.", sender)

        elif content[0:5].__eq__("<?xml"):
            self.packetHandler(content, sender)


        else:
            if self.jid.__eq__(str(msg.getFrom()).split("/")[0]):
                print "cannot answer my self with an invalid address"
            else:
                self.send("0", sender)


    def presenceHandler(self, conn,msg):

        #self.processRoster()


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

    def send(self, msg, receiver):
        self.client.send(xmpp.protocol.Message(receiver, msg))


    def packetHandler(self, message, sender):
        p = Packet.createPacketFromXml(message)

        print p.strings

        self.send(p.fr, sender)

        #try
        print ">"+p.to.strip("/")+"<"
        print p.strings
        result = self.root.getByAddress(p.to.strip("/")).use(p)
        self.send(result, sender)
        print result
        #except:
        #self.send("*"+content+" is not a valid address.", sender)

    def disconnectHandler(self):
        #
        #  ACTS A LITTLE LOONEY
        #
        print ">>>>DISCONNECT<<<<"
        if self.client.connect((self.host, self.port)) == "":
            print "not connected"
            sys.exit(0)

    def processRoster(self):

        self.rosterTree = {}


        self.roster = self.client.getRoster()

            
        for elem in self.roster.getItems():
            if not self.rosterTree.has_key(elem):
                self.rosterTree[elem]=elem
                self.send("get", elem)
                print elem