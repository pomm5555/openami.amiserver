import ConfigParser, os


class Config():

    config = ConfigParser.ConfigParser()
    config.readfp(open("server.properties"))

    # parsing jabber section
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

    # iTunesPlugin
    iTunesScript = config.get('iTunes', 'ScriptPath')

    # DefaultsPlugin
    audioPlay = config.get('Defaults', 'AudioPlay')
    audioStop = config.get('Defaults', 'AudioStop')


    # get path to script
    absPath = os.path.abspath(".")

