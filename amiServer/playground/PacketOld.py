__author__="markus"
__date__ ="$Aug 10, 2009 11:16:33 PM$"


#class Packet:
#    def __init__(self, number):
#        self.length = 0
#        self.content = {}
#        self.number = 0
#        self.numberLength = 2 #byte
#        self.lengthLength = 2 #byte
#        self.number = number
#    def __str__(self):
#        result  = str(self.number)+"("
#        result += str(self.length)+")={ "
#        for k, elem in self.content.items():
#            result += elem.__str__()+", "
#        return result+" }"
#    def addEnvelope(self, number, content):
#        self.content[number] = content
#        self.number = number
#        print self.getLength(),"&&&"
#        self.length = self.getLength()
#    def fillZero(self, string, size):
#        if string.__len__()>size:
#            print Error
#        string = str(string)
#        for i in range(0, size-string.__len__()):
#            string = "0" + string
#        return string
#    def serialize(self):
#        result  = self.fillZero(self.number, self.numberLength)
#        result += self.fillZero(self.length, self.lengthLength)
#        for k, elem in self.content.items():
#            result += elem.serialize()
#        return result
#    def initWithString(self, string):
#        print "+++"+ stf.content[number] = content
#        self.number = number
#        print self.getLength(),"&&&"
#        self.length = self.getLength()
#    def fillZero(self, string, size):
#        if string.__len__()>size:
#            print Error
#        string = str(string)
#        for i in range(0, size-string.__len__()):
#            string = "0" + string
#        return string
#    def serialize(self):
#        result  = self.fillZero(self.number, self.numberLength)
#        result += self.fillZero(self.length, self.lengthLength)
#        for k, elem in self.content.items():
#            result += elem.serialize()
#        return result
#ring
#        self.number = int(string[0:2])
#        self.length = int(string[2:4])
#        self.content = self.parseEnvelopes(string[4:])
#    def parseEnvelopes(self, string):
#        print "---"+string
#        result = {}
#        more = ""
#        len = int(string[self.numberLength:self.numberLength+self.lengthLength])
#        print "len="+str(len)
#        more = string[4+len:]
#        f = Envelope(int(string[0:2]))
#        try:
#            f.initWithString(string[4:4+len])
#        except:
#            print "ERROR::: "+string+"-+-+-+-+"
#        result[int(string[0:self.numberLength])] = f
#        if(more.__len__()>4):
#            result.update(self.parseEnvelopes(more))
#        return result
#    def fillZero(self, string, size):
#        string = str(string)
#        if string.__len__()>size:
#            print "Error"
#        for i in range(0, size-string.__len__()):
#            string = "0"+string
#        return string

class Envelope:

    def __init__(self, number=0):
        self.content = {}
        self.number = number
        self.length = 0
        self.numberLength = 2 #byte
        self.lengthLength = 2 #byte

    def __str__(self):
        result  = str(self.number)+"("
        result += str(self.length)+")=["
        for k, elem in self.content.items():
            result += elem.__str__()+","
        return result+"]"

    def initWithString(self, string):
        self.number = int(string[0:self.numberLength])
        self.length = int(string[self.numberLength:self.numberLength+self.lengthLength])
        self.content = self.parsePackets(string[self.numberLength+self.lengthLength:])

    def parsePackets(self, string): #recursive
        result = {}
        len = int(string[2:4])
        more = string[4+len:]
        f = Field(int(string[0:2]), string[4: (4+len)])
        result[int(string[0:self.numberLength])] = f
        if(more.__len__()>0):
            result.update(self.parsePackets(more))
        return result

    def serialize(self):
        result  = self.fillZero(self.number, self.numberLength)
        result += self.fillZero(self.length, self.lengthLength)
        for k, elem in self.content.items():
            result += elem.serialize()
        return result

    def addField(self, number, content):
        self.content[number] = Field(number, content)
        self.length+=content.__len__()+self.numberLength+self.lengthLength

        
    def fillZero(self, string, size):
        string = str(string)
        if string.__len__()>size:
            print "Error"
        for i in range(0, size-string.__len__()):
            string = "0"+string
        return string



class Field:

    def __init__(self, number=0, content=""):
        self.content = content
        self.number = int(number)
        self.length = content.__len__()
        self.numberLength = 2 #byte
        self.lengthLength = 2 #byte

    def initWithString(self, string):
        self.number = string[0:self.numberLength]#x = int("deadbeef", 16)
        self.content = string[self.numberLength+self.lengthLength:]
        self.length = string[self.numberLength:self.numberLength+self.lengthLength]

    def __str__(self):
        print str(type(self.content))
        print "###", self.content
        return str(self.number)+"("+str(self.length)+")="+self.content #self.serialize()

    def serialize(self):
        result =  self.fillZero(self.number, self.lengthLength) # number
        result += self.fillZero(str(self.content.__len__()), self.lengthLength) # length
        result += self.content # content
        return result

    def fillZero(self, string, size):
        string = str(string)
        if string.__len__()>size:
            print "Error"
        for i in range(0, size-string.__len__()):
            string = "0"+string
        return string