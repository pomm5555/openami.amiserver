# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="markus"
__date__ ="$Aug 21, 2009 8:15:47 PM$"

from xml.dom import minidom

if __name__ == "__main__":

    

    # Create the minidom document
    doc = Document()

    # Create the <wml> base element
    packet = doc.createElement("packet")
    packet.setAttribute("from", "none")
    packet.setAttribute("to", "/iTunes/Play")
    doc.appendChild(packet)


    # Create the main <card> element
    maincard = doc.createElement("card")
    maincard.setAttribute("id", "main")
    packet.appendChild(maincard)

    # Create a <p> element
    #paragraph1 = doc.createElement("p")
    #maincard.appendChild(paragraph1)

    # Give the <p> elemenet some text
    #ptext = doc.createTextNode("This is a test!")
    #paragraph1.appendChild(ptext)

    # Print our newly created XML
    print doc.toprettyxml(indent="  ")

