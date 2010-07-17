import avrBridgePy as avrBridgePy
import time
#get a wrapper instance
bridge = avrBridgePy.avrBridge()
#get a direct reference to libavrBridgeC
mega = bridge.mega

mega.setPortPinDir(1, 0, bridge.OUT)
mega.setPortPinDir(2, 3, bridge.OUT)
mega.setPortPinDir(2, 5, bridge.OUT)



mega.setPortPin(1, 0, bridge.ON)

print 'einschalten'
time.sleep(0.1)
mega.setPortPin(2, 3, bridge.ON)
time.sleep(10)
mega.setPortPin(2, 3, bridge.OFF)
time.sleep(1)
print 'ausschalten'
mega.setPortPin(2, 5, bridge.ON)
time.sleep(9)
mega.setPortPin(2, 5, bridge.OFF)
time.sleep(1)

mega.setPortPin(1, 0, bridge.OFF)