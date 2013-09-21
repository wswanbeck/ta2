#!/usr/bin/env python
# encoding: utf-8

import unittest
import os
import pdb
import sys
# pretend we're running from the directory above ./tests
sys.path.append(os.path.abspath('..'))
from lib.config import Config

import threading
import time
import urllib2

class FeedWatcher(threading.Thread):

    def __init__(self, feedurl):
        # when threadstop is True, thethread will stop
        self.threadstop = False

        # subscriber Urls
        self.subscriberUrls = {}

        threading.Thread.__init__(self)
        self.feedurl = feedurl

    def signalstop(self):
        self.threadstop = True
        print "Stop watching feed: " + self.feedurl

    def run(self):
        print "Start watching feed: " + self.feedurl
        while not self.threadstop:
            if len(self.subscriberUrls) > 0:
                print "== posting to subscriber"
                self.postToSubscribers()
            time.sleep(10)

    def subscribe(self, subscriberUrl, urlname):
        self.subscriberUrls[subscriberUrl] = urlname
        print "subscribed " + subscriberUrl + " " + urlname + " to feed " + self.feedurl

    def unsubscribe(self, subscriberUrl):
        try:
            # in case caller gave us a non-existant url, assume this could fail
            del self.subscriberUrls[subscriberUrl]
        except:
            pass
        print "UNsubscribed " + subscriberUrl + " to feed " + self.feedurl

    def postToSubscribers(self):
        for sub in self.subscriberUrls:
            req = urllib2.Request(sub)
            req.add_header('Content-Type', 'application/json')
            try:
                # in case something goes wrong here, we don't want to crash 
                print "posting to subscriber: " + sub + " from " + self.feedurl
                response = urllib2.urlopen(req, '{ "feedurl" : "' + self.feedurl + '"}')
            except:
                print "*** Error during post to " + sub + " ***"
                pass

class TestFeedWatcher(unittest.TestCase):

    def testStartWatchers(self):
        cfg = Config("../conf/test.conf")
        feedwatchers = []
        feedwatchers.append(FeedWatcher(cfg.feeds[0].feedurl))
        feedwatchers.append(FeedWatcher(cfg.feeds[1].feedurl))
        for fw in feedwatchers:
            fw.start()
            time.sleep(1)
        time.sleep(2)
        for alertname in cfg.watches:
            feedwatchers[0].subscribe("http://localhost:88/alert?alertname=" + alertname, "myname")
            time.sleep(1)
        time.sleep(12)
        
        for alertname in cfg.watches:
            feedwatchers[0].unsubscribe("http://localhost:88/alert?alertname=" + alertname)

        time.sleep(12)
        for fw in feedwatchers:
            fw.signalstop()

if __name__ == '__main__':
    unittest.main()

