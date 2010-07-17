# To change this template, choose Tools | Templates
# and open the template in the editor.
# growlnotify -m "hallo" -t "hallo"


import os, re
from AmiTree import Container
from PlugIn import PlugIn
from amiConfig import Config
from xml.dom.minidom import parseString
import simplejson as json
import codecs

class change(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"
        #self.override_dict ={}

        #plugin itself
        self.content = Container("plugin", token, "set something")
        self.content.rendering = Container.PLAIN

        #Plugin visibility, can be accessed, but is not listed
        self.visible = False
        
        #create a new Container
        changeElement = Container('cmd','element','ELEMENT', self.element)
        changeElement.rendering = Container.PLAIN
        changeElement.visible = True
        self.content.addChild(changeElement)
        
        
#http://localhost:8080/ami.lab@aminet.org/change/element?string={"l":"0","r":"0","d":"0","e":"name","nv":"test"}   

    def element(self, var=''):
        #declarations
        file_name = 'MyEstate'
        requestArray = {}
        
        #open and parse the file 
        try:
            file = codecs.open(Config.absPath + Config.get('XML', file_name), "r")
            xmlString = file.read()
            file.close()
            xml_object = parseString(xmlString)
        except:
            return "ERROR: FILE NOT FOUND"
        print var
        
        list = xml_object
        #building the json
        try:
            requestString = json.loads(var)
        except:
            return "ERROR: JSON SYNTAX"

        #filling the JSON into the requestArray
        for key, value in requestString.items():
            requestArray[key] = value
            print key + ': ' + value
            
        #if level is defined
        if requestArray.has_key('l'):
            #searching the levels
            for level in xml_object.getElementsByTagName('level'):
                #if requested id is in xml
                if int(requestArray['l']) >= int(xml_object.getElementsByTagName('level').length):
                    return "ERROR: OUT OF RANGE"
                #if level id == requested id
                elif level.getElementsByTagName('id')[0].firstChild.data == requestArray['l']:
                    #print level id and name to the console
                    print 'level ' + level.getElementsByTagName('id')[0].firstChild.data + ": " + level.getElementsByTagName('name')[0].firstChild.data
                    list = level
                    #if room is defined
                    if requestArray.has_key('r'):
                        #searching the rooms on the requested level
                        for room in level.getElementsByTagName('room'):
                            #if requested id is in xml
                            if int(requestArray['r']) >= int(level.getElementsByTagName('room').length):
                                return "ERROR: OUT OF RANGE"
                            #if level id == requested id 
                            elif room.getElementsByTagName('id')[0].firstChild.data == requestArray['r']:
                                #print room id and name to the console
                                print 'room ' + room.getElementsByTagName('id')[0].firstChild.data + ": " + room.getElementsByTagName('name')[0].firstChild.data
                                list = room
                                #if device is defined
                                if requestArray.has_key('d'):
                                    #searching the devices
                                    for device in room.getElementsByTagName('device'):
                                        #if requested id is in xml
                                        if int(requestArray['d']) >= int(room.getElementsByTagName('device').length):
                                            return "ERROR: OUT OF RANGE"
                                        #if device id == requested id 
                                        elif device.getElementsByTagName('id')[0].firstChild.data == requestArray['d']:
                                            #print device id and name to the console
                                            print 'device ' + device.getElementsByTagName('id')[0].firstChild.data + ": " + device.getElementsByTagName('name')[0].firstChild.data
                                            list = device
                                            #if state is defined
                                            if requestArray.has_key('s'):
                                                #searching the state
                                                for state in device.getElementsByTagName('state'):
                                                    #if requested id is in xml
                                                    if int(requestArray['s']) >= int(device.getElementsByTagName('state').length):
                                                        return "ERROR: OUT OF RANGE"
                                                    #if state id == requested id
                                                    elif state.getElementsByTagName('id')[0].firstChild.data == requestArray['s']:
                                                            #print state id and dimension to the console
                                                            print 'state ' + state.getElementsByTagName('id')[0].firstChild.data
                                                            list = state
  
        print 'old value'
        print requestArray['e'] + ': ' + list.getElementsByTagName(requestArray['e'])[0].firstChild.data
        list.getElementsByTagName(requestArray['e'])[0].firstChild.data = requestArray['nv']
        
        print 'new value'
        print requestArray['e'] + ': ' + list.getElementsByTagName(requestArray['e'])[0].firstChild.data
        
        #try to open the file and write new data
        try:
            file = open(Config.absPath + Config.get('XML', file_name), "w")
            print 'open file'
            tmp = xml_object.toxml()
            print 'object parsed'
            file.write(tmp)
            print 'file written'
            file.close()
            print 'file closed'
        except:
            return 'ERROR: NOTHING WRITTEN'
        
        print "SUCCESSFUL"
        return "SUCCESSFUL"     
               
    
    # returns the plugin as a tree
    def getTree(self):
        return self.content

    # just a little helper function
    def getText(self, var):
        try:
            var = var.strings["text"]
            return var
        except:
            return var


class Container(Container):
    def toJqHtml__(self):

            return ""
