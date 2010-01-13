# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "markus"
__date__ = "$Aug 10, 2009 11:18:56 PM$"

from Field import Field

class Envelope:

    def __init__(self, number=0):
        self.length = 0
        self.content = {}
        self.numberLength = 2 #byte
        self.lengthLength = 2 #byte
        self.number = number

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

    def serialize(self):
        result  = self.fillZero(self.number, self.numberLength)
        result += self.fillZero(self.length, self.lengthLength)
        for k, elem in self.content.items():
            result += elem.serialize()
        return result

    def addField(self, number, content):
        self.content[number] = Field(number, content)

    def parsePackets(self, string): #recursive
        result = {}
        len = int(string[self.numberLength:self.numberLength+self.lengthLength])
        more = string[4+len:]
        f = Field(int(string[0:2]), string[4: (4+len)])
        result[int(string[0:self.numberLength])] = f
        if(more.__len__()>0):
            result.update(self.parsePackets(more))
        return result

    def fillZero(self, string, size):
        string = str(string)
        for i in range(0, size-string.__len__()):
            string = "0" + string
        return string