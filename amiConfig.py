import ConfigParser, os
import logging

class Config:

    config = ConfigParser.ConfigParser()
    config.readfp(open("server.properties"))

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

    # Feed Reader
    podcasts = config.get('FeedReader', 'Podcasts')

    # get path to script
    absPath = os.path.abspath(".")

    @staticmethod
    def get(section, option):
        try:
            return Config.config.get(section, option)
        except:
            print "[CONFIG ERROR] could not get "+section+"->"+option
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
