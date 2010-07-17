# To change this template, choose Tools | Templates
# and open the template in the editor.
# growlnotify -m "hallo" -t "hallo"

from AmiTree import Container
from PlugIn import PlugIn
from amiConfig import Config
from xml.dom.minidom import parseString
import simplejson as json
import time
import PlugInsSupport.avrBridgePy as avrBridgePy

class set(PlugIn):


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
        setSTATE = Container('cmd','state','STATE', self.state)
        setSTATE.rendering = Container.PLAIN
        setSTATE.visible = True
        self.content.addChild(setSTATE)
        
        setMULTISTATE = Container('cmd','multiState','MULTISTATE', self.multiState)
        setMULTISTATE.rendering = Container.PLAIN
        setMULTISTATE.visible = True
        self.content.addChild(setMULTISTATE)
        
        
#http://localhost:8080/ami.lab@aminet.org/set/state?string={"level":"0","room":"0","device":"0","state":"0","cv":"0"}   
#http://jenskroener.homeip.net:8080/ami.lab@aminet.org/set/state?string={"level":"0","room":"0","device":"0","state":"0","cv":"0"}
    def state(self, var=''):
        #declarations
        AVR = False
        file_name = 'MyEstate'
        requestArray = {}
        channel = 'null'
        channelNumber = 'null'
        prev_temperature = 'null'
        prev_brightness = 'null'
        dimension_req = 'null'
        value_ok = False
        timestamp = ''
                
        #open and parse the file 
        try:
            file = open(Config.absPath + Config.get('XML', file_name), "r")
            xmlString = file.read()
            file.close()
            xml_object = parseString(xmlString)
            
            energy_file = open(Config.absPath + Config.get('XML', 'Energy'), "r")
            energyString =  energy_file.read()
            energy_file.close()
            energy_object = parseString(energyString)
        except:
            return "ERROR: FILE NOT FOUND"
        print var
        
        #building the json
        try:
            requestString = json.loads(var)
        except:
            return "ERROR: JSON SYNTAX"

        #filling the JSON into the requestArray
        for key, value in requestString.items():
            #check if the values are digits
            if value.isdigit():
                requestArray[key] = value
                print key + ': ' + value
            else:
                return "ERROR: VALUE IS NOT DIGIT"
        
        #creates a new element with content to the given node
        def newElement(where, element, content):
            new_element = energy_object.createElement(element)
            txt = energy_object.createTextNode(content)
            new_element.appendChild(txt)
            return where.appendChild(new_element)
        
        #writes the consumption of a device to the energy.xml
        def saveEnergy(timestamp, level, room, device, watt):
            #declarations
            level = 'level'+level
            room = 'room'+room
            device = 'device'+device   
            #time the device was on         
            hours = float(time.mktime(time.localtime()) - time.mktime(timestamp)) / 3600.0
            kw = float(watt) / 1000.0
            kwh = float(kw * hours)
            #e.g. Jan-2010
            currentMonth = str(time.strftime("%b-%Y",time.localtime()))
            
            #if the level node is in energy.xml
            if str(energy_object.getElementsByTagName(level)) != '[]':
                print 'level'
                #link the level node
                levelNode = energy_object.getElementsByTagName(level)[0]
                #and so on....
                if str(levelNode.getElementsByTagName(room)) != '[]':
                    print 'room'
                    roomNode = levelNode.getElementsByTagName(room)[0]
                    if str(roomNode.getElementsByTagName(device)) != '[]':
                        print 'device'
                        deviceNode = roomNode.getElementsByTagName(device)[0]
                        if str(deviceNode.getElementsByTagName(currentMonth)) != '[]':
                            print 'month'
                            monthNode = deviceNode.getElementsByTagName(currentMonth)[0]
                            #adds the new kwh to the old value
                            monthNode.firstChild.data = float(monthNode.firstChild.data) + float(kwh)
                            print str(kwh) + ' kWh added'
                        else:
                            #create month with kwh
                            print 'no month'
                            newElement(deviceNode, currentMonth, str(kwh))
                    else:
                        #create device, month with kwh
                        print 'no device'
                        newElement(roomNode, device, '')
                        deviceNode = roomNode.getElementsByTagName(device)[0]
                        newElement(deviceNode, currentMonth, str(kwh))
                else:
                    #create room, device, month with kwh
                    print 'no room'
                    newElement(levelNode, room, '')   
                    roomNode = levelNode.getElementsByTagName(room)[0]    
                    newElement(roomNode, device, '')
                    deviceNode = roomNode.getElementsByTagName(device)[0]
                    newElement(deviceNode, currentMonth, str(kwh))
            else:
                #create level, room, device, month with kwh
                print 'no level'
                newElement(energy_object.firstChild, level, '')
                levelNode = energy_object.getElementsByTagName(level)[0]
                newElement(levelNode, room, '')   
                roomNode = levelNode.getElementsByTagName(room)[0]    
                newElement(roomNode, device, '')
                deviceNode = roomNode.getElementsByTagName(device)[0]
                newElement(deviceNode, currentMonth, str(kwh))
                
            #save file
            try:
                energy_file = open(Config.absPath + Config.get('XML', 'Energy'), "w")
                print 'open'
                tmp1 = energy_object.toxml()
                print 'new'
                energy_file.write(tmp1)
                print 'written'
                energy_file.close()
                print 'closed'
            except:
                return 'ERROR: NOTHING WRITTEN'
            
            return ''

                  
        #searching the levels
        for level in xml_object.getElementsByTagName('level'):
            #if level id == requested id
            if level.getElementsByTagName('id')[0].firstChild.data == requestArray['l']:
                #print level id and name to the console
                print 'level ' + level.getElementsByTagName('id')[0].firstChild.data + ": " + level.getElementsByTagName('name')[0].firstChild.data
                #searching the rooms on the requested level
                for room in level.getElementsByTagName('room'):
                    #if level id == requested id 
                    if room.getElementsByTagName('id')[0].firstChild.data == requestArray['r']:
                        #print room id and name to the console
                        print 'room ' + room.getElementsByTagName('id')[0].firstChild.data + ": " + room.getElementsByTagName('name')[0].firstChild.data
                        #searching the devices
                        for device in room.getElementsByTagName('device'):
                            #if device id == requested id 
                            if device.getElementsByTagName('id')[0].firstChild.data == requestArray['d']:
                                #if a channel is defined for this device
                                if device.getElementsByTagName('channel').length != 0 :
                                    #save the channel
                                    channel = device.getElementsByTagName('channel')[0].firstChild.data
                                #if a channelNumber is defined for this device
                                if device.getElementsByTagName('channelNumber').length != 0 :
                                    #save the channelNumber
                                    channelNumber = device.getElementsByTagName('channelNumber')[0].firstChild.data
                                #print device id and name to the console
                                print 'device ' + device.getElementsByTagName('id')[0].firstChild.data + ": " + device.getElementsByTagName('name')[0].firstChild.data
                                #print channel and channelNumber to the console
                                print 'channel: ' + channel + channelNumber
                                #searching the state
                                for state in device.getElementsByTagName('state'):
                                    if state.getElementsByTagName('dimension')[0].firstChild.data == 'temperature':
                                        prev_temperature = state.getElementsByTagName('currentValue')[0].firstChild.data
                                    elif state.getElementsByTagName('dimension')[0].firstChild.data == 'brightness':
                                        prev_brightness = state.getElementsByTagName('currentValue')[0].firstChild.data
                                    #if state id == requested id
                                    if state.getElementsByTagName('id')[0].firstChild.data == requestArray['s']:
                                        #if this state is controllable
                                        if state.getElementsByTagName('controllable')[0].firstChild.data == 'true':
                                            #save the dimension
                                            dimension_req = state.getElementsByTagName('dimension')[0].firstChild.data
                                            #print state id and dimension to the console
                                            print 'state ' + state.getElementsByTagName('id')[0].firstChild.data + ": " + dimension_req
                                            #print old value to the console
                                            print 'old value: ' + state.getElementsByTagName('currentValue')[0].firstChild.data
                                            #if new and old value differs
                                            if state.getElementsByTagName('currentValue')[0].firstChild.data != requestArray['cv']:
                                                if int(requestArray['cv']) >= int(state.getElementsByTagName('minValue')[0].firstChild.data) and int(requestArray['cv']) <= int(state.getElementsByTagName('maxValue')[0].firstChild.data):
                                                    #write new value
                                                    state.getElementsByTagName('currentValue')[0].firstChild.data = requestArray['cv']
                                                    value_ok = True
                                                    #get the old timestamp
                                                    timestamp = time.strptime(str(device.getElementsByTagName('timestamp')[0].firstChild.data), "%d-%m-%Y %H:%M:%S")
                                                    #set timestamp
                                                    device.getElementsByTagName('timestamp')[0].firstChild.data = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
                                                else:
                                                    #print error
                                                    print 'ERROR: VALUE IS OUT OF MIN/MAX'
                                                    #return error
                                                    return 'ERROR: VALUE IS OUT OF MIN/MAX' 
                                            else:
                                                #print error
                                                print 'ERROR: VALUE IS ALREADY SET'
                                                #return error
                                                return 'ERROR: VALUE IS ALREADY SET'
                                            #print new value to the console
                                            print 'new value: ' + state.getElementsByTagName('currentValue')[0].firstChild.data
                                        else:
                                            return 'ERROR: NOT CONTROLLABLE'
                                        break
                                break
        
        if value_ok:
            if AVR:
                #get a wrapper instance
                self.bridge = avrBridgePy.avrBridge()
                #get a direct reference to libavrBridgeC
                self.mega = self.bridge.mega
                
                self.mega.setPortPinDir(int(Config.get("Heater", "bridgeport")), int(Config.get("Heater", "manual")), self.bridge.OUT)
                self.mega.setPortPinDir(int(Config.get("Heater", "bridgeport")), int(Config.get("Heater", "plus")), self.bridge.OUT)
                self.mega.setPortPinDir(int(Config.get("Heater", "bridgeport")), int(Config.get("Heater", "minus")), self.bridge.OUT)
                
                self.mega.setPortPinDir(int(Config.get("Remote", "channel")), int(Config.get("Remote", "a")), self.bridge.OUT)
                self.mega.setPortPinDir(int(Config.get("Remote", "channel")), int(Config.get("Remote", "b")), self.bridge.OUT)
                self.mega.setPortPinDir(int(Config.get("Remote", "channel")), int(Config.get("Remote", "c")), self.bridge.OUT)
                self.mega.setPortPinDir(int(Config.get("Remote", "channel")), int(Config.get("Remote", "d")), self.bridge.OUT)
                
                self.mega.setPortPinDir(int(Config.get("Remote", "device")), int(Config.get("Remote", "1_0")), self.bridge.OUT)
                self.mega.setPortPinDir(int(Config.get("Remote", "device")), int(Config.get("Remote", "1_1")), self.bridge.OUT)
                self.mega.setPortPinDir(int(Config.get("Remote", "device")), int(Config.get("Remote", "2_0")), self.bridge.OUT)
                self.mega.setPortPinDir(int(Config.get("Remote", "device")), int(Config.get("Remote", "2_1")), self.bridge.OUT)
                self.mega.setPortPinDir(int(Config.get("Remote", "device")), int(Config.get("Remote", "3_0")), self.bridge.OUT)
                self.mega.setPortPinDir(int(Config.get("Remote", "device")), int(Config.get("Remote", "3_1")), self.bridge.OUT)
              
            #if the device is radio controlled
            if channel != 'null' and channelNumber != 'null':
                print 'channel: ' + channel + channelNumber
                print 'channel-Port: ' + Config.get('Remote', channel)
                if AVR: self.mega.setPortPin(int(Config.get("Remote", "channel")), int(Config.get("Remote", channel)), self.bridge.ON)
                
                #possible state values: 0, 1
                if dimension_req == 'activated':
                    print 'switch to ' + requestArray['cv']
                    print 'channelNumber-Port: ' + Config.get('Remote', channelNumber + '_' + requestArray['cv'])
                    if AVR:
                        self.mega.setPortPin(int(Config.get("Remote", "device")), int(Config.get('Remote', channelNumber + '_' + requestArray['cv'])), self.bridge.ON)
                        time.sleep(0.2)
                        self.mega.setPortPin(int(Config.get("Remote", "device")), int(Config.get('Remote', channelNumber + '_' + requestArray['cv'])), self.bridge.OFF)
                        self.mega.setPortPin(int(Config.get("Remote", "channel")), int(Config.get("Remote", channel)), self.bridge.OFF)
                    #if device is swiched to 0 the consumption should be saved
                    if str(requestArray['cv']) == '0':
                        if prev_brightness == 'null':
                            print 'no brightness'
                            #save the consumption to the energy file
                            saveEnergy(timestamp, requestArray['l'], requestArray['r'], requestArray['d'], device.getElementsByTagName('watt')[0].firstChild.data)
                        else:
                            print 'brightness'
                            #calculate the consumption and write it to the energy file
                            saveEnergy(timestamp, requestArray['l'], requestArray['r'], requestArray['d'], (int(device.getElementsByTagName('watt')[0].firstChild.data)*float(int(prev_brightness)/100.0)))
                            
                #possible state values: 0-100
                elif dimension_req == 'brightness':
                    #search for the state activated
                    for state in device.getElementsByTagName('state'):
                        if str(state.getElementsByTagName('dimension')[0].firstChild.data) == 'activated':
                            #change the dim value is only allowed if activated == 1
                            if str(state.getElementsByTagName('currentValue')[0].firstChild.data) == '1':
                                print 'dim to ' + requestArray['cv']
                                #if device is swiched to another dim level the consumption should be saved
                                saveEnergy(timestamp, requestArray['l'], requestArray['r'], requestArray['d'], (int(device.getElementsByTagName('watt')[0].firstChild.data)*float(int(prev_brightness)/100.0)))
                                
                                if int(requestArray['cv']) < int(prev_brightness):
                                    #dim darker
                                    print 'channelNumber-Port: ' + Config.get('Remote', channelNumber + '_0')
                                    if AVR:                
                                        self.mega.setPortPin(int(Config.get("Remote", "device")), int(Config.get('Remote', channelNumber + '_0')), self.bridge.ON)
                                        dimTime = float(9*((float(prev_brightness)-float(requestArray['cv']))/100))
                                        time.sleep(float(dimTime))
                                        self.mega.setPortPin(int(Config.get("Remote", "device")), int(Config.get('Remote', channelNumber + '_0')), self.bridge.OFF)
                                        self.mega.setPortPin(int(Config.get("Remote", "channel")), int(Config.get("Remote", channel)), self.bridge.OFF)
                                else:
                                    #dim brighter
                                    print 'channelNumber-Port: ' + Config.get('Remote', channelNumber + '_1')
                                    if AVR:
                                        self.mega.setPortPin(int(Config.get("Remote", "device")), int(Config.get('Remote', channelNumber + '_1')), self.bridge.ON)
                                        dimTime = float(9*((float(requestArray['cv'])-float(prev_brightness))/100))
                                        time.sleep(float(dimTime))
                                        self.mega.setPortPin(int(Config.get("Remote", "device")), int(Config.get('Remote', channelNumber + '_1')), self.bridge.OFF)
                                        self.mega.setPortPin(int(Config.get("Remote", "channel")), int(Config.get("Remote", channel)), self.bridge.OFF)                                   
                                    
                                break
                            else:
                                print 'activated is 0'
                                return 'ERROR SET ACTIVATED FIRST'
                else:
                    return 'ERROR: WRONG DIMENSION'
                    
            else:#no radio controlled device
                print 'no radio controlled device'
                #heater
                if dimension_req == 'temperature':
                    print 'heater was ' + prev_temperature + ' and is set to ' + requestArray['cv'] + ' degree'
                    print 'manual-Port: ' + Config.get('Heater', 'manual')
                    if AVR:
                        self.mega.setPortPin(int(Config.get("Heater", "bridgeport")), int(Config.get("Heater", "manual")), self.bridge.ON)
                        time.sleep(0.1)
                        self.mega.setPortPin(int(Config.get("Heater", "bridgeport")), int(Config.get("Heater", "manual")), self.bridge.OFF)
                        time.sleep(0.2)
                        
                    if int(prev_temperature) < int(requestArray['cv']):
                        #raise temperature
                        for i in range(int(prev_temperature), int(requestArray['cv']) + (int(requestArray['cv']) - int(prev_temperature))):
                            print i + 1                        
                            if AVR:
                                self.mega.setPortPin(int(Config.get("Heater", "bridgeport")), int(Config.get("Heater", "plus")), self.bridge.ON)
                                time.sleep(0.1)
                                self.mega.setPortPin(int(Config.get("Heater", "bridgeport")), int(Config.get("Heater", "plus")), self.bridge.OFF)
                                time.sleep(0.1)
                            
                    else:
                        #lower temperature
                        for i in range(int(requestArray['cv']), int(prev_temperature) + (int(prev_temperature) - int(requestArray['cv']))):
                            print i + 1
                            if AVR:
                                self.mega.setPortPin(int(Config.get("Heater", "bridgeport")), int(Config.get("Heater", "minus")), self.bridge.ON)
                                time.sleep(0.1)
                                self.mega.setPortPin(int(Config.get("Heater", "bridgeport")), int(Config.get("Heater", "minus")), self.bridge.OFF)
                                time.sleep(0.1)                          
            
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

            print 'SUCCESSFUL'
            return 'SUCCESSFUL'
        else:
            print 'ERROR: OUT OF RANGE'
            return 'ERROR: OUT OF RANGE'
        
        
    test = staticmethod(state)
    
    def multiState(self, var=''):
        requestString = var[5:-1]
        response = 'SUCCESSFUL'
        tmp = ''
        print 'rS: ' + requestString
        
        def toSet(level, room, device, state, cv):
            request_to_set = '{"l":"' + level + '","r":"' + room + '","d":"' + device + '","s":"' + state + '","cv":"' + cv + '"}'
            print 'request_to_set: ' + request_to_set
            return set.test(self, request_to_set)
        
        try:
            request = json.loads(requestString)
            
        except:
            return response
        
        for key in request:
            level = str(key["id"])
            print 'level: ' + level
            
            for key in key["r"]:
                room = str(key["id"])
                print 'room: ' + room
                
                for key in key["d"]:
                    device = str(key["id"])
                    print 'device: ' + device
                    
                    for key in key["s"]:
                        state = str(key["id"])
                        cv = str(key["cv"])
                        print 'state: ' + state
                        print 'val: ' + cv
                        print 'l' + level + ' r' + room + ' d' + device + ' s' + state + ' cv' + cv
                        
                        tmp = str(toSet(level, room ,device, state, cv))
                        print 'tmp: '+tmp
                        if tmp != 'SUCCESSFUL' and tmp != 'ERROR: VALUE IS ALREADY SET':
                            if response == 'SUCCESSFUL':
                                response = '{l:' + level + ',r:' + room + ',d:' + device + ',s:' + state + ',cv:' + cv + '} ' + tmp
                            else:
                                response += ' {l:' + level + ',r:' + room + ',d:' + device + ',s:' + state + ',cv:' + cv + '} ' + tmp
    
        return response
    
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
