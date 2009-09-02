
class foo():
    def __init__(self):
        self.info = "foo"
        print "foo init"

def getInfo(self):
    return self.info


class bar():
    def __init__(self):
        self.info = "bar"
        print "bar init"



if __name__ == "__main__":
    f = foo()
    b = bar()

    b.getInfo = f.getInfo

    print f.getInfo

    #print b.getInfo()
    import code; code.interact(local=locals())
    # The output is foo, f's info attribute. I expected b to read its own info attribute.