import avrBridgePy as avrBridgePy
import time
        
#get a wrapper instance
bridge = avrBridgePy.avrBridge()
#get a direct reference to libavrBridgeC
mega = bridge.mega

mega.setPortPinDir(1, 0, bridge.OUT)
mega.setPortPinDir(1, 1, bridge.OUT)

mega.setPortPinDir(2, 0, bridge.OUT)
mega.setPortPinDir(2, 1, bridge.OUT)

mega.setPortPinDir(2, 3, bridge.OUT)
mega.setPortPinDir(2, 5, bridge.OUT)



print 'channel A on'
mega.setPortPin(1, 0, bridge.ON)

time.sleep(1)

print 'dev 1 on'
mega.setPortPin(2, 0, bridge.ON)
time.sleep(0.2)
mega.setPortPin(2, 0, bridge.OFF)

time.sleep(1.5)

print 'dev 1 off'
mega.setPortPin(2, 1, bridge.ON)
time.sleep(0.2)
mega.setPortPin(2, 1, bridge.OFF)
time.sleep(1.5)


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


print 'channel A off'
mega.setPortPin(1, 0, bridge.OFF)


time.sleep(2)

print 'channel B on'
mega.setPortPin(1, 1, bridge.ON)

time.sleep(1)

print 'dev 2 on'
mega.setPortPin(2, 0, bridge.ON)
time.sleep(0.2)
mega.setPortPin(2, 0, bridge.OFF)

time.sleep(1.5)

print 'dev 2 off'
mega.setPortPin(2, 1, bridge.ON)
time.sleep(0.2)
mega.setPortPin(2, 1, bridge.OFF)
time.sleep(1.5)

print 'channel B off'
mega.setPortPin(1, 1, bridge.OFF)