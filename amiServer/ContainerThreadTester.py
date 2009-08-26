from AmiTree import *
import time

__author__="markus"
__date__ ="$Aug 26, 2009 7:23:39 AM$"


# method that is used as run later
def test(text = "hallo"):
    while 1:
        print text
        time.sleep(1)

# you can make a child for Threadcontainer and overwrite the run method
class testContainer(ThreadContainer):
    def run(self):
        while 1:
            print self.information
            time.sleep(3)

if __name__ == "__main__":

    # creating a container to host the tree
    root = Container("root", "root")

    
    # create a threadcontainer for passing the run method via setDo
    # params: node-type, container-token, container-information
    t = ThreadContainer("thread", "thread", "test")
    # set run method via setDo method
    t.setDo(test)
    # start thraded node
    t.start()
    # add to root container
    root.addChild("thread", "thread", t)

    # create testContainer what is a threaded container with a overwritten run method
    # params: node-type, container-token, container-information
    t2 = testContainer("thread", "polymorph", "this is a polymorph shidt whatever")
    # start thread node
    t2.start()
    # add testContainer instance to root container
    root.addChild("thread", "polymorph", t2)

    # print the tree structure
    print root.returnTree(0)


