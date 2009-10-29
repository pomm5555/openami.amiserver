import ConfigParser, os
import logging

class Config:

    config = ConfigParser.ConfigParser()
    filename = "server.properties"
    file = open(filename, "r")
    config.readfp(file)
    file.close()

    # parsing jabber section the old way, should not be used anymore
    jid = config.get('jabber', 'jid')
    pwd = config.get('jabber', 'pwd')
    host = config.get('jabber', 'host')
    port = config.get('jabber', 'port')
    ressource = config.get('jabber', 'ressource')
    groupChat = config.get('jabber', 'groupChat')
    groupServer = config.get('jabber', 'groupServer')

    # parsing system section
    token = config.get('server', 'token')
    information = config.get('server', 'information')
    architecture = config.get('server', 'architecture')

    # parsing plugins section
    plugInsFolder = config.get('Plugins', 'PlugInsFolder')

    #avrLib
    avrLib = config.get('avrBridge', 'lib')

    # iTunesPlugin
    iTunesScript = config.get('iTunes', 'ScriptPath')

    # DefaultsPlugin
    audioPlay = config.get('Defaults', 'AudioPlay')
    audioStop = config.get('Defaults', 'AudioStop')
    setVol = config.get('Defaults', 'SetVol')
    Notification = config.get('Defaults', 'Notification')

    # get path to script
    absPath = os.path.abspath(".")


    @staticmethod
    def save():
        Config.file = open(Config.filename, "w")
        Config.config.write(Config.file)
        Config.file.close()

    @staticmethod
    def setOption(section, option, value):
        if not Config.config.has_section(section):
            Config.config.add_section(section)
        Config.config.set(section, option, value)
        Config.save()    

    @staticmethod
    def get(section, option):
        try:
            return Config.config.get(section, option)

        except ConfigParser.NoOptionError:
            Config.setOption(section, option, "PLEASE_DEFINE_THIS")
            print "[CONFIG ERROR] could not get "+section+"->"+option
            return "error"

    @staticmethod
    def getSection(section):
        try:
            return Config.config.items(section)
        except ConfigParser.NoSectionError:
            Config.config.add_section(section)
            Config.save()
            print "[CONFIG ERROR] could not get section "+section
            print "section created"
            return "error"

if __name__ == "__main__":
    logger = logging.getLogger("Config")
    logger.info("--------------------")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    #create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    #add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    print(Config.getSection("FeedReader"))
    print(Config.get("FeedReader", "cre"))
