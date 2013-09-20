#!/usr/bin/env python
# encoding: utf-8

import unittest
import os
import pdb
import sys
# pretend we're running from the directory above ./tests
sys.path.append(os.path.abspath('..'))
from lib.config import Config

from threading import Thread
import time

class FeedWatcher:

    # when threadstop is True, thethread will stop
    threadstop = False

    def __init__(self, feedurl):
        self.feedurl = feedurl

    def start(self):
        self.thread = Thread(target = self.thethread)
        self.thread.start()

    def stop(self):
        self.threadstop = True
        self.thread.join()
        print "Stopped watching feed: " + self.feedurl

    def thethread(self):
        while not self.threadstop:
            print "Watching feed: " + self.feedurl
            time.sleep(10)

class TestFeedWatcher(unittest.TestCase):

    def test1(self):
        cfg = Config("../conf/test.conf")
        feedwatchers = []
        feedwatchers.append(FeedWatcher(cfg.feeds[0].feedurl))
        feedwatchers.append(FeedWatcher(cfg.feeds[1].feedurl))
        for fw in feedwatchers:
            fw.start()
        time.sleep(2)
        for fw in feedwatchers:
            fw.stop()

if __name__ == '__main__':
    unittest.main()

