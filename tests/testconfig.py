#!/usr/bin/env python
# encoding: utf-8

import unittest
import os
import pdb
import sys
# pretend we're running from the directory above ./tests
sys.path.append(os.path.abspath('..'))
from lib.config import Config

class TestConfig(unittest.TestCase):

    def test1(self):
        cfg = Config("../conf/test.conf")
        # verify that config had 2 watches specified in it
        self.assertEqual(len(cfg.watches), 2)

if __name__ == '__main__':
    unittest.main()
