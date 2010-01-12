__author__="markus"
__date__ ="$Aug 10, 2009 11:19:24 PM$"

class Field:
    
    def __init__(self, number=0, content=""):
        self.numberLength = 2 #byte
        self.lengthLength = 2 #byte
        self.content = content
        self.number = number
        self.length = content.__len__()

    def initWithString(self, string):
        self.number = string[0:2]#x = int("deadbeef", 16)
        self.content = string[4:]
        self.length = string[2:4]

    def __str__(self):
        return str(self.number)+"("+str(self.length)+")="+self.content #self.serialize()

    def serialize(self):
        result =  self.fillZero(self.number, self.lengthLength) # number
        result += self.fillZero(str(self.content.__len__()), self.lengthLength) # length
        result += self.content # content
        return result

    def fillZero(self, string, size):
        string = str(string)
        for i in range(0, size-string.__len__()):
            string = "0"+string
        return string

