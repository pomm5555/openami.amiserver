#!/usr/bin/python

import os, sys, logging

l = logging.getLogger()
logging.basicConfig(filename="test.log", level=logging.DEBUG)

test1 = logging.getLogger("test.hallo")
test2 = logging.getLogger("test.naechster")
test3 = logging.getLogger("test.sonst")
l.info("test")
test1.warn("hallo")
test2.info("mein")
test3.debug("name ist test")


