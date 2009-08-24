from xml.dom.minidom import *
from Packets.Packet import Packet

# http://wiki.python.org/moin/MiniDom

if __name__ == "__main__":


    p = Packet("fernmelder@jabber.org", "servant@jabber.org/Finder/Say")
    p.addString("text1", "Hello master")
    p.addString("text2", "How are you")
    print p

    print("2---")
    #deserialize data
    p2 = Packet.createPacketFromXml(p.__str__())
    print p2.fr
    print p2.to
    #print p2.strings[0]


    for k,v in p.strings.items():
        print k+"="+v
