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
from bottle import route, run

@route('/', method='GET')
def homepage():
    return 'Hello World'

@route('/alert/:alertname', method='POST')
def post_alert(alertname):
    return dict(name='what to say now...')

class TestConductor(unittest.TestCase):

    def test1(self):
        run(host='localhost', port=88)

if __name__ == '__main__':
    unittest.main()
