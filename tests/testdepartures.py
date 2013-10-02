#!/usr/bin/env python
# encoding: utf-8

import unittest
import os
import sys
import urllib2
# pretend we're running from the directory above ./tests
sys.path.append(os.path.abspath('..'))
import lib.commuterraildisplayboard

class TestConductor(unittest.TestCase):

    def test1(self):

        csvfile = open("testdata/testDepartures.csv")
        csvdata = csvfile.read()
        csvfile.close()

        self.assertTrue(lib.commuterraildisplayboard.CommuterRailDisplayBoard.GetDeparture('341', csvdata), "Should have found an entry for trip 341")
        self.assertFalse(lib.commuterraildisplayboard.CommuterRailDisplayBoard.GetDeparture('999', csvdata), "Should not have found an entry for trip 999")

        # check more details
        trip341 = lib.commuterraildisplayboard.CommuterRailDisplayBoard.GetDeparture('341', csvdata)
        self.assertEqual(trip341['Origin'], 'North Station')
        self.assertEqual(trip341['Destination'], 'Lowell')
        self.assertEqual(trip341['ScheduledTime'], '1380673800')
        self.assertEqual(trip341['Lateness'], '0')
        self.assertEqual(trip341['Track'], '')
        self.assertEqual(trip341['Status'], 'On Time')

    def atest2(self):
        trip = '341'

        f_url = urllib2.urlopen('http://developer.mbta.com/lib/gtrtfs/Departures.csv')
        csvdata = f_url.read()
        f_url.close()

        trip341 = lib.commuterraildisplayboard.CommuterRailDisplayBoard.GetDeparture('341', csvdata, "This is only true when trip 341 is active since it's live data")
        self.assertTrue(trip341, "This will not always be true - depends on what time of day we run this test")

if __name__ == '__main__':
    unittest.main()
