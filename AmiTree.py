# To change this template, choose Tools | Templates
# and open the template in the editor.

from threading import Thread
from Address import Address
from amiData import *
import types
import logging
import logging.config
from amiConfig import Config

__author__="markus"
__date__ ="$Aug 16, 2009 3:56:03 PM$"

class Container:

    PLAIN = 0
    JQ = 1


    def __init__(self, type, token, information="empty", use=None, args="none", logging=False):
        self.content = {}
        self.information = information
        self.token = token.replace(" ", "_")
        self.type = type
        self.visible = True
        self.parent = None
        self.logging = logging
        self.addresslist = None
        # how should webengine render the containers content jq|plain...
        self.rendering = Container.JQ
        self.use_args=args
        if use:

            self.setUse(use)

        # bei der initialisierung ist getAddress noch auf token beschraekt weil parent noch nicht besetzt oder so
        # TODO
        self.collector = Data.getCollector(self.getAddress())

        

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
        data = self.useL(unspecified)
        if self.logging:
            self.collector.log(data.__str__())
        return data

    def useL(self, unspecified=""):
        return self.information

    def setUseArgs(self, args):
        self.use_args =args
        
    def setUse(self, use, use_args=None):
        #self.use = use
        self.use_args = use_args
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
            return "<container type=\""+self.type+"\" token=\""+self.token+"\">"+result+"</container>"
        else:
            return ""

    def toHtml(self):
        if self.visible:
            result=""
            for k, v in self.content.items():
                result+=v.toHtml()

            return "<ul class='rounded'><li><a href=\""+self.getAddress()+"\">"+self.token+"</a></li>"+result+"</ul>"
        else:
            return ""

    def toJqHtml(self):

        if self.visible and not self.content == {}:

            result=""
            for k, v in self.content.items():
                result+=v.toJqHtml()

            address = self.getAddress().replace("/", "_").replace("@", "_").replace(".", "_")
            token = self.token
			
	    home = self.root().token.replace("/","_").replace("@","_").replace(".","_")

            if self.token.__eq__("root"):
                backbutton = ''
            else:
                backbutton = "<a class='back' href='#'>Back</a>"

            homebutton=""#"<a href='#root'><img class='cam' style='-webkit-user-select: none' src='http://192.168.1.239:8081/' height=30 width=40></a>"#<a class='notsoleftButton' href='#"+home+" '>Home</a>"

            toolbar = "<div class='toolbar'><h1 style='opacity:1;'>"+token+"</h1>"+backbutton+homebutton+"<a class='togglefloaty button slideup' href='#about'>More</a></div>"
            content = "<ul class='rounded'>"
            for k, v in self.content.items():

                if not v.content == {}:
                    content += "<li class='arrow'><a class='' href='#"+v.getAddress().replace("/", "_").replace("@", "_").replace(".", "_")+"'>"+k+"</a></li>"

                else:
                    test = None
                    try: #TODO better error handling, when method toJqHtmlElement throws error, no exception is be thrown
                        test = v.toJqHtmlElement
                    except AttributeError:
#absolut addressing                        content += "<li><a class='' target='_self' href='http://"+Config.systemIp+":"+Config.systemPort+"/"+v.getAddress()+"'>"+k+"</a></li>"
                        content += "<li><a class='' target='_self' href='"+v.getAddress()+"'>"+k+"</a></li>"
                    if test:
                        content += v.toJqHtmlElement()

            content += "</ul>"
            content += "<div class='info'>"+self.information+"</div>"
            html = "<div id='"+address+"'>"+toolbar+content+"</div>"+result

            return html

        else:
            return ""

    
    # add container without creating it first, token, information and optionally a method that is triggered.
    def addContainer(self, type, token, information="empty", use=None, args="none",logging=False):
        self.addChild(Container(type, token, information,args=args, logging=logging))
        if use:
            self.getChild(token).setUse(use)
            

    def getAddressList(self):
        if not self.addresslist:
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

            self.addresslist = addressList
            return addressList
        return self.addresslist

    def parent(self):
        return self.parent

    def root(self):
        if self.parent:
            return self.parent.root()
        else:
            return self

    def getAddress(self):        
        # TODO Address-cache would be useful
        address = self.RgetAddress()
        return address[address.find("/")+1:]
    
    def RgetAddress(self):
        if self.parent:
            #print "this is NOT root...-->"+self.token
            return  self.parent.RgetAddress()+"/"+self.token
        else:
            #print "this is root...-->"+self.token
            return self.token

    # TODO Dirty!!! gehoert hier nicht her!!! oder doch, mal konzept ueberlegen...
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
        self.daemon = False


    def setDo(self, method):
        #self.run = method
        self.run = types.MethodType(method.im_func, self, self.__class__)


    def run(self):
        pass

class BuddyContainer(Container):
    def __init__(self, type, token, information, send):
        Container.__init__(self, type, token, information)
        self.send = send

    def use(self, msg=""):
        message=self.token+"/"+self.information+" "+msg
        print 'sending: '+message
        self.send(message, self.token)

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


class SwitchContainer(Container):

    def __init__(self, type, token, information="empty", use=None, logging=False, on=None, off=None, checked=True):
        Container.__init__(self, type, token, information, use, logging)
        self.on = on
        self.off = off
        self.checked = checked

    def toJqHtmlElement(self):
        if self.visible:
            checkedStr = ''
            if self.checked == True:
                checkedStr = " checked=\'checked\'"
            content = '<li>'+self.token+'<span class="toggle"><input type="checkbox" onChange="if(this.checked) $.get(\''+self.on+'\');else $.get(\''+self.off+'\');"' + checkedStr + '/></span></li>'
            return content
        else:
            return ""

    def setChecked(self, checked):
        self.checked = checked

class CheckBoxContainer(Container):

    def __init__(self, type, token, information=None, use=None, logging=False, toogle=None, checked=True):
        Container.__init__(self, type, token, information, use, logging)
        if information==None:
            self.information = token
        self.checked = checked
        self.toogle = toogle

    def toJqHtmlElement(self):
        if self.visible:
            checkedStr = ''
            if self.checked == True:
                checkedStr = ' checked=\"checked\"'
            content = '<li><input type=\"checkbox\" onChange="if(this.checked) $.get(\''+self.toogle+'?string=True\');else $.get(\''+self.toogle+'?string=False\');" title=\"' + self.information + '\"' + checkedStr + '/></li>'
            return content
        else:
            return ""

    def setChecked(self, checked):
        self.checked = checked

class TextfieldContainer(Container):

    def __init__(self, type, token, information="empty", use=None, logging=False, target=None, value=""):
        Container.__init__(self, type, token, information, use, logging)
        self.target = target
        self.value = value

    def toJqHtmlElement(self):
        if self.visible:
            content = '<li><input type="text" name="'+self.token+'" placeholder="'+self.token+'" id="sole_name" onBlur="$.get(\''+self.target+'?string=\'+$(this).val());" value="'+self.value+'"/></li>'
            return content
        else:
            return ""

    def setValue(self, value):
        self.value = value
