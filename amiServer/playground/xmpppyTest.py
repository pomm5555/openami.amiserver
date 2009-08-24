import xmpp
import sys
import xmpp
import signal
import time
from Ami_tree import Container
from Plugins import ITunes

#jid=xmpp.protocol.JID("servant@jabber.org")
#cl=xmpp.Client(jid.getDomain())
#
#cl.connect()
#cl.auth(jid.getNode(),"servantjabbers")
#
#cl.sendInitialPresence(jid, None, 1)
#cl.send(xmpp.protocol.Message("mt034@messi.mi.hdm-stuttgart.de","first message from ami_ce"))



def messageCB(conn,msg):
    content = str(msg.getBody())
    sender = str(msg.getFrom())
    print "Sender: " + sender
    print "Content: " + content

    print content[0:1]
    print content[1:]

    if content.__eq__("get"):
        send(root.returnTree(0), sender)
    if content[0:1].__eq__("*"):
        root.getByAddress(content[1:]).use()

def stepOn(conn):
    try:
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
    global recipient
    global root
    root = Container("192.168.1.1", "Tree Root")
    # create library object
    t = ITunes("ITunes")
    # Add ITunes Plugin to tree
    root.addChild("ITunes", t.getTree())

    jid="servant@jabber.org"
    pwd="servantjabbers"

    jid=xmpp.protocol.JID(jid)

    global cl
    cl = xmpp.Client(jid.getDomain(), debug=[])

    if cl.connect() == "":
        print "not connected"
        sys.exit(0)

    if cl.auth(jid.getNode(),pwd) == None:
        print "authentication failed"
        sys.exit(0)
    cl.RegisterHandler('message', messageCB)

    cl.sendInitPresence()

    goOn(cl)

main()
