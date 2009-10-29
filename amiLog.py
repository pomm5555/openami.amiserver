import logging
from amiConfig import Config

class InfoLogger:
    #logging.basicConfig(filename=Config.get("infologger", "file"), level=logging.DEBUG)
    logging.info("logging initialized")

    # File Formatter
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

    # File Handler
    fh = logging.FileHandler(filename="test.log", mode="a")
    fh.setFormatter(formatter)

    # Info Logger
    infologger = logging.getLogger("info")
    infologger.setLevel(logging.DEBUG)
    infologger.addHandler(fh)
    infologger.info("filelogging initialized")

if __name__ == "__main__":
    l = InfoLogger()
    test = logging.getLogger()
    test.info("hallo test")

    test2 = logging.getLogger("info")
    test2.info("hallo dies ist der 2. test")

    test3 = logging.getLogger("info.test2")
    test3.info("mensch, ich hoff das klappt jetzt mal")
    
