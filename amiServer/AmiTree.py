# To change this template, choose Tools | Templates
# and open the template in the editor.

from threading import Thread
import xmpp

__author__="markus"
__date__ ="$Aug 16, 2009 3:56:03 PM$"

class Container:

    def __init__(self, type, token, information="empty"):
        self.content = {}
        self.information = information
        self.token = token
        self.type = type
        self.visible = True

    def __str__(self):
        return self.information

    def addChild(self, container):
        self.content[container.token] = container
        self.content[container.token].type = container.type

    def addChildList(self, containers):
        for elem in containers:
            self.addChild(elem)

    def getChild(self, token):
        try:
            return self.content[token]
        except:
            print "[ERROR] Token "+token+" is not a child of "+str(type(self))

    def getByAddress(self, address):
        print self,
        print ": ",
        print dir(self)
        print type(self)
        number = address.find("/")
        if not number == -1:
            token = address[:number]
            restAddress = address[number+1:]
            print token+"---"+restAddress+"--"
            
            return self.getChild(token).getByAddress(restAddress)
        else:
            return self.getChild(address)


    def use(self, unspecified=""):
        return self.information

    def setUse(self, use):
        self.use = use

    def printTree(self, i):
        print self.visible
        for elem in range(0,i):
                print "  ",
        print "* "+self.token+"("+str(self)+")"
        i+=1
        for k, v in self.content.items():
            v.printTree(i)

    def returnTree(self, i):

        ret = ""

        for elem in range(0,i):
                ret += "-"

        if self.visible:
            ret += "* "+self.token+"("+str(self.information)+")\n"

        i+=1

        for k, v in self.content.items():
            ret += str(v.returnTree(i))
        return str(ret)

    def toXml(self):
        if self.visible:
            result=""
            for k, v in self.content.items():
                result+=v.toXml()
            return "<container type=\""+self.type+"\" token=\""+self.token+"\" information=\""+self.information+"\">"+result+"</container>"
        else:
            return ""

    # add container without creating it first, token, information and optionally a method that is triggered.
    def addContainer(self, type, token, information="empty", use=None):
        self.addChild(Container(type, token, information))
        if not use==None:
            self.getChild(token).setUse(use)


    def getAddressList(self):
        result = []
        print self.visible
        for k,v in self.content.items():
            if v.visible:
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

class BuddyContainer(Container):
    def __init__(self, type, token, information, client):
        Container.__init__(self, type, token, information)
        self.client = client

    def use(self, msg=""):
        self.client.send(xmpp.protocol.Message(self.token, self.token+"/"+self.information+" "+msg))

    def getByAddress(self, address):
        #print "+++++"+address
        self.information = address
        return self

        