#!/usr/bin/python
'''
Integration test, testing the functionality of models.bart.py:BartRestApi.
'''

import unittest
from flask_app.models import bart

class Test_etd(unittest.TestCase):

    def setUp(self):
        self.station = 'mont'

    def test_returns_xml(self):
        etd_xml = bart.BartRestApi.etd(self.station)
        #print etd_xml

        self.assertTrue(
            etd_xml.startswith('<?xml version="1.0" encoding="utf-8"?>'))

    def test_returns_correct_uri(self):
        etd_xml = bart.BartRestApi.etd(self.station)

        uri_str = '<uri><![CDATA[http://api.bart.gov/api/etd.aspx?' \
                  'cmd=etd&orig=%s]]></uri>' % (self.station)
        self.assertTrue(uri_str in etd_xml)

class Test_stations(unittest.TestCase):

    def test_return_correct_xml(self):
        stations_xml = bart.BartRestApi.stations()

        self.assertTrue(
            stations_xml.startswith('<?xml version="1.0" encoding="utf-8"?>'))

    def test_return_correct_uri(self):
        stations_xml = bart.BartRestApi.stations()

        uri_str = '<uri><![CDATA[http://api.bart.gov/api/stn.aspx?' \
                  'cmd=stns]]></uri>'

        self.assertTrue(uri_str in stations_xml)

if __name__ == '__main__':
    unittest.main()
