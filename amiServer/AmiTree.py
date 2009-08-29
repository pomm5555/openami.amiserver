# To change this template, choose Tools | Templates
# and open the template in the editor.

from threading import Thread

__author__="markus"
__date__ ="$Aug 16, 2009 3:56:03 PM$"

class Container:

    def __init__(self, type, token, information="empty"):
        self.content = {}
        self.information = information
        self.token = token
        self.type = type

    def __str__(self):
        return self.information

    def addChild(self,type, token, container):
        self.content[token] = container
        self.content[token].type = type

    def getChild(self, token):
        try:
            return self.content[token]
        except:
            print "[ERROR] Token "+token+" is not a child of "+str(type(self))

    def getByAddress(self, address):
        c = self
        for elem in address.split("/"):
            c = c.getChild(elem)
        return c

    def use(self):
        return self.__str__()

    def setUse(self, use):
        self.use = use

    def printTree(self, i):
        for elem in range(0,i):
                print "  ",
        print "* "+self.token+"("+str(self)+")"
        i+=1
        for k, v in self.content.items():
            v.printTree(i)

    def returnTree(self, i):
        ret = ""
        for elem in range(0,i):
                ret += " "
        ret += "* "+self.token+"("+str(self)+")\n"
        i+=1
        for k, v in self.content.items():
            ret += str(v.returnTree(i))
        return str(ret)

    def toXml(self):
        result=""
        for k, v in self.content.items():
            result+=v.toXml()
        return "<container type=\""+self.type+"\" token=\""+self.token+"\" information=\""+self.information+"\">"+result+"</container>"

    # add container without creating it first, token, information and optionally a method that is triggered.
    def addContainer(self, tt, token, information="empty", use=None):
        self.addChild(tt, token, Container(tt, token, information))
        self.getChild(token).setUse(use)

    def getAddressList(self):
        result = []
        for k,v in self.content.items():
            result += v.getAddressList()

        # if result list is empty, its a leaf
        if not result:
            result.append(self.token)
            return result

        # it is not a leaf...
        tmp = []
        for elem in result:
            tmp.append(self.token+"/"+elem)

        return tmp



class ThreadContainer(Container, Thread):
    def __init__(self, type, token, information="empty"):
        Container.__init__(self, type, token, information)
        Thread.__init__(self, None)


    def setDo(self, method):
        self.run = method

    def run(self):
        pass
        