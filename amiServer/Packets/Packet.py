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

        return dom.toprettyxml()


    def addString(self, name, string):
        self.strings[name] = string
        

    @staticmethod
    def createPacketFromXml(string):
        dom = parseString(string).documentElement

        #print packets from adderess
        fr =  dom.attributes["from"].value
        #print packets to address
        to =  dom.attributes["to"].value

        p = Packet(fr, to)

        for elem in dom.childNodes:
            if elem.nodeType == elem.ELEMENT_NODE:
                content = elem.firstChild.data
                print content
                p.addString(elem.attributes["name"], content)

        return p
