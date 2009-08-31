import xmpp
import sys, time
from Packets.Packet import Packet
from amiConfig import Config
from Address import Address

class CommunicationEngine:

    def __init__(self, root):

        self.root = root

	# last time ping was sent, initialisation
	self.last_time = 0
	self.keepalive = 1

        self.jid=xmpp.protocol.JID(Config.jid)
        self.client = xmpp.Client(self.jid.getDomain())

        # connect client
        if self.client.connect((Config.host, Config.port)) == "":
            print "not connected"
            sys.exit(0)

        # authenticate client
        if self.client.auth(self.jid.getNode(), Config.pwd, Config.ressource) == None:
            print "authentication failed"
            sys.exit(0)

        # register message handler
        self.client.RegisterHandler('message', self.messageHandler)

        #init roster
        self.processRoster()

        # set presencehandler and presence
        self.client.RegisterHandler('presence', self.presenceHandler)
        self.client.sendInitPresence()

        # register disconnect handler
        self.client.RegisterDisconnectHandler(self.disconnectHandler)


        room = Config.groupChat+"@"+Config.groupServer+"/"+Config.jid.split("@")[0]
        print "Joining groupchat: " + room
        self.client.send(xmpp.Presence(to=room))

        print "Communicationengine is online, or should be... #TODO" #TODO

        # go to eventLoop
        self.goOn(self.client)

    def pingJabber(self):
        try:
	    now = int(time.strftime('%s', time.localtime()))
	    if self.last_time == 0:
	        self.last_time = now
	    delta = now - self.last_time
	    if delta>self.keepalive:
	    	#self.client.send(' ')
		self.client.sendPresence(self.jid, "can i send a message here?")
		print "sent some presence"
                self.last_time = now
	except Exception,e:
	    print "[ERROR] could not send ping"
	    print e

    def messageHandler(self, conn, msg):
        print "---message--------------------------------------------------"
        #print unicode(dir(msg))
        #print unicode(msg.getFrom()).split("/")[0]
        #print " "+self.jid

        # extractint content from message
        content = unicode(msg.getBody())
        sender = unicode(msg.getFrom())
        type = unicode(msg.getType())
        self.chat = ""

        try:
            if type.__eq__("groupchat"):
                print "GROUPCHAT!!!!!!"
                self.chat = sender.split("/")[0]
                print "chat: "+self.chat
        except Exception, e:
            print "[ERROR] sender: "+sender
            print e



        print "("+type+") Sender: " + sender + "\n Content: " + content


        # try to parse ass Address
        addr = Address(content)
        
        if content.__eq__("show"):
            print " parsing as show command"
            self.send(self.root.returnTree(0), sender)

        elif content.__eq__("xml"):
            print " parsing as xml command"
            self.send(self.root.me.toXml(), sender)

        elif content.__eq__("list"):
            print " parsing as list command"
            result = ""
            for elem in self.root.me.addressIndex:
                result += elem+"\n"
            self.send(result, sender)

        elif content.__eq__("help"):
            print " parsing as help command"
            help = '''
enter:
help to print this message
xml to print xml representation
show to print message overview
list to print all available addresses

search:
enter search command with * before
eg "*play"

Use following XML to sent a Packet:
<?xml version="1.0" ?>
<packet from="fernmelder@jabber.org" to="/Finder/Say">
  <string name="text">
    Hello master, my name is hal2000
  </string>
</packet>
            '''
            self.send(help, sender)

        elif addr.isAddress():
            print " parsing as address command: "+addr.__str__()
            print " with data: >"+addr.string+"<"
            try:
                if addr.string.__len__() == 0:
                    result = self.root.getByAddress(addr.__str__()).use("")
                else:
                    result = self.root.getByAddress(addr.__str__()).use(addr.string)
                self.send(result, sender)
                print " "+str(result)
            except Exception, e:
                self.send("[ERROR] "+content+" is not a valid address.", sender)
                print "[ERROR] "+str(e)


        elif content[0:1].__eq__("*"):
            print " parsing as search command"
            result = []
            answer = ""

            # seperate search string form data string
            searchstring = content.split(" ")[0][1:]
            datastring = ""
            for elem in content.split(" ")[1:]:
                datastring += " "+elem
            datastring = datastring[1:]

            print "'"+searchstring+"' - '"+datastring+"'"

            # search in address index for searchstring and build a list with resulting addresses
            for elem in self.root.me.addressIndex:
                if not elem.lower().find(searchstring.lower()) == -1:
                    result.append(elem)

            # if there is only one address resulting, execute it
            if result.__len__() == 1:
                answer = " executing: "+result[0]
                try:
                    if datastring.__len__() == 0:
                        tmp = str(self.root.getByAddress(result[0]).use(""))
                    else:
                        tmp = str(self.root.getByAddress(result[0]).use(datastring))

                    if not tmp == None:
                        answer+="\n"+str(tmp)
                    self.send("executing: "+result[0], sender)
                except Exception, e:
                    print "[ERROR] "+str(e)

            # otherwise return result to sender
            else:
                for elem in result:
                    answer += elem+"\n"
                self.send(answer, sender)



        elif content[0:5].__eq__("<?xml"):
            print " parsing as packet command"
            self.packetHandler(content, sender)


        else:
            print "unknown command"
            if self.jid.__eq__(str(msg.getFrom()).split("/")[0]):
                print " cannot answer my self with an invalid address"
            else:
                # with two bots, that causes an endless loops
                pass#self.send(" unknown command", sender)

        print "---message end----------------------------------------------"


    def presenceHandler(self, conn,msg):
        print str(msg)
        prs_type=msg.getType()
        who=msg.getFrom()
        if prs_type == "subscribe":
            conn.send(xmpp.Presence(to=who, typ = 'subscribed'))
            conn.send(xmpp.Presence(to=who, typ = 'subscribe'))

    def stepOn(self, conn):
        try:
            conn.Process(1)
	    self.pingJabber()
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
        if self.client.connect((Config.host, Config.port)) == "":
            print "not connected"
            sys.exit(0)

    def processRoster(self):

        self.rosterTree = {}


        self.roster = self.client.getRoster()

            
        for elem in self.roster.getItems():
            if not self.rosterTree.has_key(elem):
                self.rosterTree[elem]=elem
                self.send("Hello Master!\nI'm on, and waiting for your orders.\nEnter 'help' to explore me.", elem)
                print elem
