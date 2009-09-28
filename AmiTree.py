# To change this template, choose Tools | Templates
# and open the template in the editor.

from threading import Thread
from Address import Address
import types

__author__="markus"
__date__ ="$Aug 16, 2009 3:56:03 PM$"

class Container:

    def __init__(self, type, token, information="empty", use=None):
        self.content = {}
        self.information = information
        self.token = token.replace(" ", "_")
        self.type = type
        self.visible = True
        self.parent = None
        if use:
            self.setUse(use)
        


    def __str__(self):
        return self.information

    def index(self):
        return self.information

    index.exposed = True

    def addChild(self, container):
        container.type = container.type
        container.parent = self
        self.content[container.token] = container

    def addChildList(self, container):
        for elem in container:
            self.addChild(elem)

    def getChild(self, token):
        try:
            return self.content[token]
        except:
            print "[ERROR] Token "+token+" is not a child of "+self.__str__()

    def getParent(self):
        return self.parent

    def getByAddress(self, address):
        #print self
        #print ": ",
        #print dir(self)
        #print type(self)

        #complete address
        #address = Address(address).__str__()

        number = address.find("/")
        if not number == -1:
            token = address[:number]
            restAddress = address[number+1:]
            #print token+"---"+restAddress+"--"
            
            return self.getChild(token).getByAddress(restAddress)
        else:
            return self.getChild(address)


    def use(self, unspecified=""):
        return self.useL(unspecified)

    def useL(self, unspecified=""):
        return self.information


    def setUse(self, use):
        #self.use = use
        self.useL = types.MethodType(use.im_func, self, self.__class__)

    def printTree(self, i):
        #print self.visible
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
            return "<container token=\""+self.token+"\">"+result+"</container>"
        else:
            return ""

    def toHtml(self):
        if self.visible:
            result=""
            for k, v in self.content.items():
                result+=v.toHtml()

            return "<ul><li><a href=\""+self.getAddress()+"\">"+self.token+"</a></li>"+result+"</ul>"
        else:
            return ""
    
    # add container without creating it first, token, information and optionally a method that is triggered.
    def addContainer(self, type, token, information="empty", use=None):
        self.addChild(Container(type, token, information))
        if use:
            self.getChild(token).setUse(use)


    def getAddressList(self):
        result = []
        #print self.visible
        for k,v in self.content.items():
            if v.visible:
                result += v.getAddressList()

        # if result list is empty, its a leaf
        if not result:
            result.append(self.token)
            return result

        # it is not a leaf...
        addressList = []
        for elem in result:
            addressList.append(self.token+"/"+elem)

        return addressList


    def root(self):
        if self.parent:
            return self.parent.root()
        else:
            return self

    def getAddress(self):
        address = self.RgetAddress()
        return address[address.find("/")+1:]
    
    def RgetAddress(self):
        if self.parent:
            #print "this is NOT root...-->"+self.token
            return  self.parent.RgetAddress()+"/"+self.token
        else:
            #print "this is root...-->"+self.token
            return self.token

    # TODO Dirty!!! gehoert hier nicht her!!!
    def getText(self, var):
        try:
            var = var.strings["text"]
            return test
        except:
            return var


class ThreadContainer(Thread, Container):
    def __init__(self, type, token, information="empty"):
        Thread.__init__(self, None)
        Container.__init__(self, type, token, information)


    def setDo(self, method):
        #self.run = method
        self.run = types.MethodType(method.im_func, self, self.__class__)


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


class loggingContainer(Container):

    def __init__(self, type, token, information):
        Container.__int__(self, type, token, information)
        self.log = []

    def use(self, string=""):
        result = ""
        for elem in self.log:
            result += elem+"\n"

        return result


        
