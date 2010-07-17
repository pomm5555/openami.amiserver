import avrBridgePy as avrBridgePy
import time
        
#get a wrapper instance
bridge = avrBridgePy.avrBridge()
#get a direct reference to libavrBridgeC
mega = bridge.mega

mega.setPortPinDir(0, 0, bridge.OUT)
mega.setPortPinDir(0, 4, bridge.OUT)
mega.setPortPinDir(0, 5, bridge.OUT)

mega.setPortPin(0, 0, bridge.OFF)
mega.setPortPin(0, 4, bridge.OFF)
mega.setPortPin(0, 5, bridge.OFF)

print 'manual'
mega.setPortPin(0, 0, bridge.ON)
time.sleep(0.1)
mega.setPortPin(0, 0, bridge.OFF)

time.sleep(3)

print 'plus'
mega.setPortPin(0, 4, bridge.ON)
time.sleep(0.1)
mega.setPortPin(0, 4, bridge.OFF)

time.sleep(3)

print 'minus'
mega.setPortPin(0, 5, bridge.ON)
time.sleep(0.1)
mega.setPortPin(0, 5, bridge.OFF)