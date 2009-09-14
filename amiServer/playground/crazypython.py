
class foo():
    def __init__(self):
        self.info = "foo"
        print "foo init"
        children = {}


    def getInfo(self):
        return self.info


    def newFoo(self, func):
        new = Foo()
        new.getInfo = func
        children.appned(new)

    def __str(self):
        print self.info
        for elem in children:
            print " ",
            print elem


class bar():
    def __init__(self):


        if __name__ == "__main__":
            f = foo()
            b = foo()

            b.getInfo = f.getInfo

            print f.getInfo

            #print b.getInfo()
            import code; code.interact(local=locals())
