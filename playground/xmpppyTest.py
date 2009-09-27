# coding: utf-8
import sys
import xmpp





def messageHandler(conn,msg):
    #content = msg.getBody().__str__().encode( "utf-8" )
    #print type(msg.getBody().__str__())
    #content = unicode(msg.getBody(), "utf8")#"iso-8859-1")

    print "*"

    if msg.getBody():


        try:
            content = msg.getBody().encode("iso-8859-1")
        except (UnicodeDecodeError, UnicodeEncodeError):
            content=u""
            #conn.send(xmpp.Message(uin,reply.decode(kodow)))

        #import code; code.interact(local=locals())

        sender = unicode(msg.getFrom())
        print "Sender: " + sender
        print "Content: " + content

        send (content, sender)

def disconnectHandler(self):
    print ">>>>DISCONNECT HANDLER<<<<"
    if not self.client.isConnected():
        print "reconnecting..."
        self.client.reconnectAndReauth()

def stepOn(conn):
    try:
        print "checking connection"
        if not cl.isConnected():
            print "trying reconnect..."
            cl.reconnectAndReauth()
        conn.Process(1)
    except KeyboardInterrupt:
        return 0
    return 1

def goOn(conn):
    while stepOn(conn):
        pass

def send(msg, sender):
    cl.send(xmpp.protocol.Message(sender,msg.decode("iso-8859-1")))


def main():
    print "Š"

    print "start"
    global recipient

    jid="servant@jabber.org"
    pwd="servantjabbers"

    jid=xmpp.protocol.JID(jid)

    global cl
    cl = xmpp.Client(jid.getDomain(), debug=[])
    
    print "cl defiend, trying to connect"

    if cl.connect() == "":
        print "not connected"
        sys.exit(0)
    
    print "connected"

    if cl.auth(jid.getNode(),pwd) == None:
        print "authentication failed"
        sys.exit(0)
    cl.RegisterHandler('message', messageHandler)
    cl.RegisterDisconnectHandler(disconnectHandler)

    print "authenticated"

    cl.sendInitPresence()

    goOn(cl)

main()
