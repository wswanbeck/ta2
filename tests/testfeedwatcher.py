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
from lib.feedwatcher import FeedWatcher, FeedWatcherManager

class TestFeedWatcher(unittest.TestCase):

    def testStartWatchers(self):
        fm = FeedWatcherManager()
        cfg = Config("../conf/test.conf")
        fm.init(cfg)
        fm.start()
        time.sleep(2)
        for alertname in cfg.watches:
            fm.subscribe(cfg.watches[alertname].watch_feed_name,"http://localhost:88/alert?alertname=" + alertname, alertname)
            time.sleep(1)
        time.sleep(12)
        
        for alertname in cfg.watches:
            fm.unsubscribe(cfg.watches[alertname].watch_feed_name,"http://localhost:88/alert?alertname=" + alertname)

        time.sleep(12)
        fm.stop()

if __name__ == '__main__':
    unittest.main()

