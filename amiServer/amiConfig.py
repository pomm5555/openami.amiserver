import ConfigParser


class Config():

    config = ConfigParser.ConfigParser()
    config.readfp(open("server.properties"))

    # parsing jabber section
    jid = config.get('jabber', 'jid')
    pwd = config.get('jabber', 'pwd')
    host = config.get('jabber', 'host')
    port = config.get('jabber', 'port')
    ressource = config.get('jabber', 'ressource')

    # parsing system section
    token = config.get('server', 'token')
    information = config.get('server', 'information')

    # parsing plugins section
    plugInsFolder = config.get('Plugins', 'PlugInsFolder')

    # iTunesPlugin
    iTunesScript = config.get('iTunes', 'ScriptPath')

