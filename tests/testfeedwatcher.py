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
        while not self.threadstop:
            print "==== " + self.feedurl + " " + str(len(self.subscriberUrls))
            if len(self.subscriberUrls) > 0:
                print "Watching feed: " + self.feedurl
            else:
                print "NOT watching feed: " + self.feedurl
            time.sleep(10)

    def subscribe(self, subscriberUrl, urlname):
        self.subscriberUrls[subscriberUrl] = urlname
        print "subscribed " + subscriberUrl + " " + urlname + " to feed " + self.feedurl

    def unsubscribe(self, subscriberUrl):
        del self.subscriberUrls[subscriberUrl]
        print "UNsubscribed " + subscriberUrl + " to feed " + self.feedurl



class TestFeedWatcher(unittest.TestCase):

    def testStartWatchers(self):
        cfg = Config("../conf/test.conf")
        feedwatchers = []
        feedwatchers.append(FeedWatcher(cfg.feeds[0].feedurl))
        feedwatchers.append(FeedWatcher(cfg.feeds[1].feedurl))
        for fw in feedwatchers:
            fw.start()
        time.sleep(2)
        feedwatchers[0].subscribe("testurl", "myname")
        time.sleep(12)

        feedwatchers[0].unsubscribe("testurl")
        time.sleep(12)
        for fw in feedwatchers:
            fw.signalstop()

if __name__ == '__main__':
    unittest.main()

