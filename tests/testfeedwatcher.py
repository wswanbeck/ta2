#!/usr/bin/env python
# encoding: utf-8

import unittest
import os
import pdb
import sys
import time
# pretend we're running from the directory above ./tests
sys.path.append(os.path.abspath('..'))
from lib.config import Config
from lib.feedwatcher import FeedWatcher

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

