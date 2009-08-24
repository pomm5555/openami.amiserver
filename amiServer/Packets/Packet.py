from xml.dom.minidom import *


class Packet:



    def __init__(self, fr, to):

        self.fr = fr
        self.to = to

        self.strings = {}

    def __str__(self):

        # Create the minidom document
        dom = Document()

        # Create the <wml> base element
        packet = dom.createElement("packet")
        packet.setAttribute("from", self.fr)
        packet.setAttribute("to", self.to)

        # creating string tags
        for key, value in self.strings.items():
            stringTag = dom.createElement("string")
            stringTag.setAttribute("name", key)

            # Add Text to Tag
            tagText = dom.createTextNode(value)
            stringTag.appendChild(tagText)

            packet.appendChild(stringTag)
        
        dom.appendChild(packet)

        return dom.toprettyxml(indent="  ")


    def addString(self, name, string):
        self.strings[name] = string
        

    @staticmethod
    def createPacketFromXml(string):
        dom = parseString(string) #.documentElement

        #print packets from adderess
        fr =  dom.firstChild.attributes["from"].value
        #print packets to address
        to =  dom.firstChild.attributes["to"].value

        p = Packet(fr, to)

        # get all string data
        #print "---"+dom.firstChild.toxml()
        for elem in dom.firstChild.childNodes:
            print "1>"+str(dir(elem))
            print "2>"+str(type(elem))
            #stringContent = elem.firstChild.data
            #print type(stringContent)
            #print stringContent
            #p.addString(elem.attributes["name"], elem.firstChild.data)

        return p
