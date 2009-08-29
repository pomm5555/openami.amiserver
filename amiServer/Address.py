import re
from amiConfig import Config

def main():
    a = Address("/test")
    print a.tokens
    print a.string
    print a
    if a.isAddress():
        print "we habe a packet"


class Address:

    def __init__(self, addr):

        self.tokens = []
        self.string = ""
        self.valid = False
        
        patLocal = re.compile(r"^(/\w+)+.*")
        patAbs = re.compile(r"\w*@\w*.\w{2,4}(/\w+)*.*")

        # parse absolute addressed address
        if not patAbs.match(addr) == None:

            # has string
            if not addr.find(" ")==-1:
                self.string = addr[addr.find(" ")+1:]
                addr = addr[:addr.find(" ")]

            # fill tokens
            self.tokens = addr.split("/")

            # set packet valid
            self.valid = True


        # parse local addressed address
        elif not patLocal.match(addr) == None:
            # has string
            if not addr.find(" ")==-1:
                self.string = addr[addr.find(" ")+1:]
                addr = addr[:addr.find(" ")]

            #fill tokens
            self.tokens = addr.split("/")
            self.tokens[0] = Config.jid

            # set packet valid
            self.valid = True




    def __str__(self):
        if self.valid:
            result = ""
            for elem in self.tokens:
                result += "/"+elem

            return result[1:]
        else: return ""

    def isAddress(self):
        return self.valid

if __name__ == "__main__":
    main()