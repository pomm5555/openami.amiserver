
class container():
    def __init__(self):
        #print "foo init"
        self.info = "undefiend info attribute"

    def use(self):
        print self.info


class tree():
    def __init__(self):

        # create container instance
        b = container()

        # change b's info attribute
        b.info = "b's info attribute"

        # bound method test is set as use of b and in this case unbound, i think
        b.use = self.test

        # should read b's info attribute and print it
        print b.use()

    # bound method test
    def test(self):
        return "test: "+self.info


if __name__ == "__main__":
    b = tree()
