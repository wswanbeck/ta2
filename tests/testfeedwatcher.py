#!/usr/bin/env python
# encoding: utf-8

import unittest
import os
import pdb
import sys
# pretend we're running from the directory above ./tests
sys.path.append(os.path.abspath('..'))
# from lib.config import Config

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
        print "thread stopped"

    def thethread(self):
        while not self.threadstop:
            print "Thread running"
            time.sleep(1)

class TestFeedWatcher(unittest.TestCase):

    def test1(self):
        fw = FeedWatcher("someurl")
        fw.start()
        time.sleep(2)
        fw.stop()

if __name__ == '__main__':
    unittest.main()

