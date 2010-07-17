# To change this template, choose Tools | Templates
# and open the template in the editor.
# growlnotify -m "hallo" -t "hallo"

from AmiTree import Container
from PlugIn import PlugIn
from amiConfig import Config
from xml.dom.minidom import parseString
import simplejson as json
import codecs
import time

class get(PlugIn):

    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"

        #plugin itself
        self.content = Container("plugin", token, "get something")
        self.content.rendering = Container.PLAIN

        #Plugin visibility, can be accessed, but is not listed
        self.visible = True
        
        getSTATE = Container('cmd','state','STATE', self.state)
        getSTATE.rendering = Container.PLAIN
        getSTATE.visible = True
        self.content.addChild(getSTATE)
    
        getENERGY = Container('cmd','energy','ENERGY', self.energy)
        getENERGY.rendering = Container.PLAIN
        getENERGY.visible = True
        self.content.addChild(getENERGY)

    def state(self, var=''):
        #declarations
        file_name = 'MyEstate'
        requestArray = {}
        response = "ERROR: OUT OF RANGE"
        
        #open and parse the file 
        try:
            file = codecs.open(Config.absPath + Config.get('XML', file_name), "r")
            xmlString = file.read()
            file.close()
            xml_object = parseString(xmlString)
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
                        #print room id and name on the console
                        print 'room ' + room.getElementsByTagName('id')[0].firstChild.data + ": " + room.getElementsByTagName('name')[0].firstChild.data
                        #overwrites the error text with the JSON start
                        response = '{d:['      
                        #searching the devices           
                        for device in room.getElementsByTagName('device'):
                            #print device id and name to the console 
                            print 'device ' + device.getElementsByTagName('id')[0].firstChild.data + ": " + device.getElementsByTagName('name')[0].firstChild.data
                            #JSON: device id and beginning of state
                            response += '{id:' + device.getElementsByTagName('id')[0].firstChild.data + ',s:['
                            #searching the states
                            for state in device.getElementsByTagName('state'):
                                #print state id and its current Value to the console
                                print 'state ' + state.getElementsByTagName('id')[0].firstChild.data + ": value: " + state.getElementsByTagName('currentValue')[0].firstChild.data
                                #JSON: state id and its current Value
                                response += '{id:' + state.getElementsByTagName('id')[0].firstChild.data + ',cv:' + state.getElementsByTagName('currentValue')[0].firstChild.data + '}'
                                #if this is the last state
                                if (str(state.getElementsByTagName('id')[0].firstChild.data) == str(device.getElementsByTagName('state').length - 1)):
                                    #JSON: close the device
                                    response += ']}'
                                else:
                                    #JSON: continue with next state
                                    response += ','
                            #if this is the last device
                            if (str(device.getElementsByTagName('id')[0].firstChild.data) == str(room.getElementsByTagName('device').length - 1)):
                                #JSON: close the room
                                response += ']}'
                            else:
                                #JSON continue with next device
                                response += ','            
        print 'return: ' + response
        return response 

    
    def energy(self, var=''):
        #declarations
        file_name = 'MyEstate'
        requestArray = {}
        #watt, kwh, costs
        wattsRoom = [0, 0, 0]
        
        #month as string: Jan-2010
        currentMonth = time.strftime("%b-%Y", time.localtime())
        #month as int: 6
        current_month = int(time.strftime("%m", time.localtime()))
        returnString = ''
        
        
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
            requestArray[key] = value
            print key + ': ' + value
        
        #save the price
        price = float(xml_object.getElementsByTagName('pricePerkWh')[0].firstChild.data)
        
        #return watt, kwh and costs for the given device
        def getWatts(device, levelID, roomID, deviceID, currentMonth = currentMonth, energy_object = energy_object, requestArray = requestArray, price = price):
            #watt = watt, kWh, costs
            getwatts = [0,0,0]
            dim = 'null'
            act = 'null'
            levelID = 'level'+levelID
            roomID = 'room'+roomID
            deviceID = 'device'+deviceID
            #saves the brightness and activated states
            for state in device.getElementsByTagName('state'):
                if str(state.getElementsByTagName('dimension')[0].firstChild.data) == 'brightness':
                    dim = state.getElementsByTagName('currentValue')[0].firstChild.data
                if str(state.getElementsByTagName('dimension')[0].firstChild.data) == 'activated':
                    act = state.getElementsByTagName('currentValue')[0].firstChild.data
            #if device is turned on
            if act == '1':  
                #if device is dimable       
                if dim != 'null':
                    #calculate watt
                    watt = (int(device.getElementsByTagName('watt')[0].firstChild.data)*float(int(dim)/100.0))
                else:
                    #return watt
                    watt = device.getElementsByTagName('watt')[0].firstChild.data
                #calculations
                hours = float(time.mktime(time.localtime()) - time.mktime(time.strptime(str(device.getElementsByTagName('timestamp')[0].firstChild.data), "%d-%m-%Y %H:%M:%S"))) / 3600.0
                kw = float(watt) / 1000.0
                kwh = float(kw * hours)
                #fill in calculatet stuff
                getwatts[0] = int(watt)
                getwatts[1] = float(kwh)
            #search for older consumptions
            #try if the level is already there
            eLevel = energy_object.getElementsByTagName(levelID)
            if str(eLevel) != '[]':
                #and so on ...
                eRoom = eLevel[0].getElementsByTagName(roomID)
                if str(eRoom) != '[]':
                    eDevice = eRoom[0].getElementsByTagName(deviceID)
                    if str(eDevice) != '[]':
                        #so the device is already in energy file
                        if requestArray.has_key('m'):
                            #if older months are requested
                            months = int(requestArray['m'])
                            #calculate the oldest month
                            oldestMonth = current_month-months
                            #for each month between oldest month and current month
                            for months in range(oldestMonth, current_month):
                                #if months of last year are requested
                                if months < 1:
                                    months = 12 + months
                                    if months<10:
                                        #add a 0 and current year -1
                                        tmp = '0' + str(months) + '-' + str(int(time.strftime("%Y", time.localtime()))-1)
                                    else:
                                        #add current year -1
                                        tmp = str(months) + '-' + str(int(time.strftime("%Y", time.localtime()))-1)
                                else:
                                    if months<10:
                                        #add a 0 and current year
                                        tmp = '0' + str(months) + time.strftime("-%Y", time.localtime())
                                    else:
                                        #add current year
                                        tmp = str(months) + time.strftime("-%Y", time.localtime())
                                #node = get month in Jan-2010 format from tmp, which is in 01-2010 format
                                node = eDevice[0].getElementsByTagName(time.strftime("%b-%Y",time.strptime(tmp, "%m-%Y")))
                                print str(node)
                                #if month is there
                                if str(node) != '[]':
                                    txt = node[0].firstChild.data
                                    #add the consumption of this month to the consumption of the device
                                    getwatts[1] = float(getwatts[1]) + float(txt)
                        else:
                            #if no months are requested add only the current month
                            eMonth = eDevice[0].getElementsByTagName(currentMonth)
                            if str(eMonth) != '[]':
                                getwatts[1] = float(getwatts[1]) + float(eMonth[0].firstChild.data)
            
            #calculate the costs
            getwatts[2] = float(getwatts[1]) * float(price)
            #round the float values
            getwatts[0] = round(float(getwatts[0]), 3)
            getwatts[1] = round(float(getwatts[1]), 3)
            getwatts[2] = round(float(getwatts[2]), 3)
            print levelID + ' ' + roomID + ' ' + deviceID + ': ' + str(getwatts[0]) + ' watt; ' + str(getwatts[1]) + ' kWh; ' + str(getwatts[2]) + ' Euro'
            return getwatts
        

        #if more than 12 months are requestet return error
        if requestArray.has_key('m'):
            if int(requestArray['m']) > 12:
                return 'ERROR: TOO MANY MONTHS'
            if int(requestArray['m']) < 1:
                return 'ERROR: TOO FEW MONTHS'
        
        #if a level is requested
        if requestArray.has_key('l'):
            returnString = '{d:['
            #search the levels
            for level in xml_object.getElementsByTagName('level'):
                #if requested id is in xml
                if int(requestArray['l']) >= int(xml_object.getElementsByTagName('level').length):
                    return "ERROR: OUT OF RANGE"
                #save levelID
                levelID = str(level.getElementsByTagName('id')[0].firstChild.data)
                print 'level '+levelID
                if levelID == requestArray['l']:
                    #search the rooms
                    for room in level.getElementsByTagName('room'):
                        #if requested id is in xml
                        if int(requestArray['r']) >= int(level.getElementsByTagName('room').length):
                            return "ERROR: OUT OF RANGE"
                        #save room ID
                        roomID = str(room.getElementsByTagName('id')[0].firstChild.data)
                        if roomID == requestArray['r']:
                            print 'room '
                            #search the devices
                            for device in room.getElementsByTagName('device'):
                                deviceID = str(device.getElementsByTagName('id')[0].firstChild.data)
                                print'device '+deviceID
                                #get the watts, kwh and costs
                                tmp = getWatts(device, levelID, roomID, deviceID)
                                #build json return string with the consumption data
                                returnString += '{id:' + deviceID + ',watt:' + str(tmp[0]) + ',kwh:' + str(tmp[1]) + ',eur:' + str(tmp[2]) + '}'
                                #if this is the last deivce of this room
                                if deviceID == str(room.getElementsByTagName('device').length -1):
                                    returnString += ']}'
                                else:
                                    returnString += ','
                            break
                    break                          
        #if no level is requested
        else:
            returnString = '{l:['
            #for each level
            for level in xml_object.getElementsByTagName('level'):
                #save the ID
                levelID = str(level.getElementsByTagName('id')[0].firstChild.data)
                returnString += '{id:' + levelID + ',r:['
                #for each room
                for room in level.getElementsByTagName('room'):
                    #save the ID
                    roomID = str(room.getElementsByTagName('id')[0].firstChild.data)
                    returnString += '{id:' + roomID
                    #clear the arrays
                    wattsRoom[0] = 0
                    wattsRoom[1] = 0
                    wattsRoom[2] = 0
                    #for each device
                    for device in room.getElementsByTagName('device'):
                        #save the ID
                        deviceID = str(device.getElementsByTagName('id')[0].firstChild.data)
                        #get the consumption data
                        tmp = getWatts(device, levelID, roomID, deviceID)
                        #adds the consumption data of each device to the room arrays
                        wattsRoom[0] = float(wattsRoom[0]) + float(tmp[0])
                        wattsRoom[1] = float(wattsRoom[1]) + float(tmp[1])
                        wattsRoom[2] = float(wattsRoom[2]) + float(tmp[2])
                    #build json with the data
                    returnString += ',watt:' + str(wattsRoom[0]) + ',kwh:' + str(wattsRoom[1]) + ',eur:' + str(wattsRoom[2]) + '}'
                    #if this is the last room of this level
                    if roomID != str(level.getElementsByTagName('room').length -1):
                        returnString += ','
                #json: close the roomarray and write the level consumtions                       
                returnString += ']}'
                #if this is the last level
                if levelID == str(xml_object.getElementsByTagName('level').length -1):
                    #json: close the levelarray and write the "residence" consumtions                       
                    returnString += ']}'
                else:
                    returnString += ','
                    
        print 'return: ' + returnString
        return returnString
        

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

