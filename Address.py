import re
from amiConfig import Config

def main():
    adl= ('/test',
          'ami.client@jabber.org/test some data which can be got from Address.data',
          'servant@jabber.org',
          'was weiss ich')
          
    for elem in adl:
        a = Address(elem)
        print a.data
        print a.__str__()
        if a.isAddress():
            print "we have an Address\n\n\n\n"
        else:
            print "address is not valid\n\n\n"


class Address:

    def __init__(self, addr):

        self.tokens = []
        self.data = ""
        self.valid = False
        
        patLocal = re.compile(r"^(/\w+)+.*")
        patAbs = re.compile(r".*?@\w*.\w{2,4}(/\w+)*.*")

        # parse absolute addressed address
        if not patAbs.match(addr) == None:

            # has data
            if not addr.find(" ")==-1:
                self.data = addr[addr.find(" ")+1:]
                addr = addr[:addr.find(" ")]

            # fill tokens
            self.tokens = addr.split("/")

            # set packet valid
            self.valid = True


        # parse local addressed address
        elif not patLocal.match(addr) == None:
            # has data
            if not addr.find(" ")==-1:
                self.data = addr[addr.find(" ")+1:]
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