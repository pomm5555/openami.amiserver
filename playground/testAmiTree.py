# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "markus"
__date__ = "$Aug 13, 2009 11:02:27 PM$"


from Ami_tree import Container
from Plugins import ITunes
import os



# Mute instanciates Container and overwrites the use() method
class Mute(Container):
    def use(self):
        os.system("osascript -e 'set volume output muted false'  ")

def test():
    print "test"

# Create a container
root = Container("192.168.1.1", "Tree Root")

# add a child container
root.addChild("token.1", Container("token.1", "someContent"))

# returns roots information string: "empty"
print root

# output: "someContent"
print root.getChild("token.1")

# use use() that by default prints the information string "someContent" the information
# string could be regularly updated by a thread that pushes the actual temperatur or something
root.getChild("token.1").use()

# set test() method as new use() method
root.getChild("token.1").setUse(test)

# test() prints "test" to the console
root.getChild("token.1").use()

# create library object
t = ITunes("ITunes")

# use this method of lib as new use method
root.getChild("token.1").setUse(t.unmute)

# mute iTunes =)
root.getChild("token.1").use()

# add a Mute-container to root container
root.addChild("token.2", Mute("token.2", "This could execute also easily shellscripts"))

# mute iTunes
root.getChild("token.2").use()

# print information of the container token.2
print root.getChild("token.2")

# add a child to token.1
root.getChild("token.1").addChild("test", Container("test","gotMe"))

# address it by a slashpath
print root.getByAddress("token.1/test")

print "-----------"

# print tree representation of container and its childs
root.printTree(0)


print "-----------"
# Add ITunes Plugin to tree
root.addChild("ITunes", t.getTree())
root.printTree(0)
root.getByAddress("ITunes/Play").use()


print "************"
# print xml representation of content, no idea weather its useful...
print root.toXml

print "***"+root.returnTree(0)
