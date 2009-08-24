from xml.dom.minidom import *
from Packets.Packet import Packet

# http://wiki.python.org/moin/MiniDom

if __name__ == "__main__":


    p = Packet("fernmelder@jabber.org", "servant@jabber.org/Finder/Say")
    p.addString("text1", "Hello master")
    p.addString("text2", "How are you?")
    print p

    print ("1---")
    #get xml header
    #print p.__str__().split("\n")[0]

    
    print("2---")
    #deserialize data
    p2 = Packet.createPacketFromXml(p.__str__())
    print p2.fr
    print p2.to
    #print p2.strings[0]

    #print packets from adderess
    #print p2.getElementsByTagName("packet")[0].attributes["from"].value
    #print packets to address
    #print p2.getElementsByTagName("packet")[0].attributes["to"].value

    #print "3---"

    #get some sub xml
    #print p2.childNodes[0].toxml()

    #print "4---"

    # get first string elements tag name
    #print p2.g&etElementsByTagName("string")[0].tagName

    # get string elements capabilities
    #print dir(p2.getElementsByTagName("string")[0])


    # get all string data
    #for elem in p2.getElementsByTagName("string"):
    #    print ">"+elem.firstChild.data.strip(" \n")+"<"

