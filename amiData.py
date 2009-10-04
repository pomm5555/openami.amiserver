# To change this template, choose Tools | Templates
# and open the template in the editor.
import time


class Collector:

    def __init__(self, channel):
        self.channel = channel

    def log(self, data):
        Data.log(self.channel, data)

class Data:
    type = "file" # file | sqlite
    file = "logs/data.log"
    console = "true"

    # Collector Factory
    @staticmethod
    def getCollector(channel):
        col = Collector(channel)
        return col


    # Selects to which location logging is passed to
    @staticmethod
    def log(channel, data):
        if Data.type.__eq__("file"):
            Data.logfile(channel, data)

        if Data.type.__eq__("sqlite"):
            print "loggingtype not suppported"

        if Data.console.__eq__("true"):
            print time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())+" - "+channel+" - "+data

    @staticmethod
    def logfile(channel, data):
        file = open(Data.file, "a")
        print str(type(channel))
        print str(type(data))
        string = "<time>"+time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())+"</time><channel>"+channel+"</channel><data>"+data+"</data>\n"
        file.write(string)
        file.flush()
        file.close()


if __name__ == "__main__":
    col = Data.getCollector("test")
    #import code; code.interact(local=locals())
    col.log("testest")
