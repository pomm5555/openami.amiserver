from Packet import *

class test:
    def test(self):
        print "test"

if __name__ == "__main__":


    print "\n\n+++ envelope testing +++"

    f = Envelope(1)
    g = Envelope(55)


    g.addField(11, "schweinsoehrchen") 
    g.addField(3, "sauerbraten")
    print g

    serializedG = g.serialize()
    print serializedG

    f.initWithString(serializedG)
    print str(f)

    e = Envelope(0)
    print e, 1
    
    print e, 2
    e.addField(77, "Weihnachtsgans")
    print e, 4
    print e.serialize()

