#!/usr/bin/env python
# encoding: utf-8

import unittest
import os
import pdb
import sys
# pretend we're running from the directory above ./tests
sys.path.append(os.path.abspath('..'))
from lib.config import Config

import bottle
from bottle import route, run, request
import threading
import urllib2

@route('/', method='GET')
def homepage():
    return 'Hello World'

@route('/watch/:watchname', method='POST')
def post_alert(watchname):
    try:
        thiswatch = Config("../conf/test.conf").watches[watchname]
        if thiswatch.watchtype == "vehicle-assigned":
            watchtrip = thiswatch.trip
            for message in request.json["Messages"]:
                if message["Trip"] == str(watchtrip):
                    if message["Vehicle"] != "":
                        print "=== alert: Vehicle for trip " + str(watchtrip) + " is " + message["Vehicle"] + " ==="
    except:
        pass
    return dict(name='watchname = ' + watchname)

# this doesn't actually work - I wonder how to make this work
@route('/quit', method='GET')
def get_quit():
    exit()

def runconductor():
    pass

# Run the REST server in a thread
# just instantiate this class and call .start(portnumber)
# e.g. 
#  a = RESTServer()
#  a.start(88)  # listen on port 88
#
# there's currently no way to stop it once it starts though
class RESTServer(threading.Thread):

    def __init__(self, portnumber):
        self.portnumber = portnumber
        threading.Thread.__init__(self)

    def run(self):
        run(host="localhost", port=self.portnumber)

# You need to run this as sudo!!
class TestConductor(unittest.TestCase):

    def test1(self):
        # setup subscribers (but don't actually start up feed watcher)
        # conductor = Conductor(Config("../conf/test.conf"))
        config = Config("../conf/test.conf")
        # startup the conductor
        # run(reloader=False, host='localhost', port=88)
        rs = RESTServer(91)
        rs.start()
        print "started..."

        self.post("watch-a")

        self.post("watch-b")

        # run tests
        print "tests completed.  Press control-C (a bunch of times) to quit this test"

    def post(self, watchname):
        url = "http://localhost:91/watch/" + watchname
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        try:
            feed = ""
            with open("testdata/testMBTAfeed.json") as f:
                feed = f.read()
            print "posting to: " + url
            response = urllib2.urlopen(req, feed)
        except Exception, e:
            print "*** Error " + str(e) + " during post to " + url + " ***"
            pass
        

if __name__ == '__main__':
    unittest.main()
