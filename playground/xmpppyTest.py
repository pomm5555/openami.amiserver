import sys
import xmpp



def messageHandler(conn,msg):
    content = unicode(msg.getBody())
    sender = unicode(msg.getFrom())
    print u"Sender: " + sender
    print u"Content: " + content

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
    cl.send(xmpp.protocol.Message(sender,msg))


def main():
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
