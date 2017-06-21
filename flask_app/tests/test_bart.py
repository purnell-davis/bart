#!/usr/bin/python
'''
Functional test, testing the functionality of bart.py.
'''

import unittest
import bart
from mock import patch
from mock import MagicMock

SAMPLE_XML = \
'''<?xml version="1.0" encoding="utf-8"?>
<root>
    <uri><![CDATA[http://api.bart.gov/api/etd.aspx?cmd=etd&orig=rich]]></uri>
    <date>01/20/2014</date>
    <time>04:17:19 PM PST</time>
    <station>
        <name>Richmond</name>
        <abbr>RICH</abbr>
        <etd>
            <destination>Daly City</destination>
            <abbreviation>DALY</abbreviation>
            <estimate>
                <minutes>8</minutes>
                <platform>2</platform>
                <direction>South</direction>
                <length>5</length>
                <color>RED</color>
                <hexcolor>#ff0000</hexcolor>
                <bikeflag>1</bikeflag>
            </estimate>
            <estimate>
                <minutes>28</minutes>
                <platform>2</platform>
                <direction>South</direction>
                <length>5</length>
                <color>RED</color>
                <hexcolor>#ff0000</hexcolor>
                <bikeflag>1</bikeflag>
            </estimate>
        </etd>
        <etd>
            <destination>Fremont</destination>
            <abbreviation>FRMT</abbreviation>
            <estimate>
                <minutes>17</minutes>
                <platform>2</platform>
                <direction>South</direction>
                <length>6</length>
                <color>ORANGE</color>
                <hexcolor>#ff9933</hexcolor>
                <bikeflag>1</bikeflag>
            </estimate>
            <estimate>
                <minutes>37</minutes>
                <platform>2</platform>
                <direction>South</direction>
                <length>6</length>
                <color>ORANGE</color>
                <hexcolor>#ff9933</hexcolor>
                <bikeflag>1</bikeflag>
            </estimate>
        </etd>
    </station>
    <message/>
</root>
'''

class Test_schedule(unittest.TestCase):

    @patch('bart.requests.get')
    def test_dict_is_correct(self, requests_mock):
        requests_mock.return_value = MagicMock(text=SAMPLE_XML)
        expected_dict = {'station_name': 'Richmond',
                         'station_abbr': 'RICH',
                         'destinations': [
                             {'destination_name': 'Daly City',
                              'destination_abbr': 'DALY',
                              'direction': 'South',
                              'color': 'RED',
                              'hexcolor': '#ff0000',
                              'estimates': [
                                {'minutes': '8', 
                                 'length': '5'},
                                {'minutes': '28', 
                                 'length': '5'}]},
                             {'destination_name': 'Fremont',
                              'destination_abbr': 'FRMT',
                              'direction': 'South',
                              'color': 'ORANGE',
                              'hexcolor': '#ff9933',
                              'estimates': [
                                {'minutes': '17', 
                                 'length': '6'},
                                {'minutes': '37', 
                                 'length': '6'}]}]}

        self.assertEquals(bart.schedule('rich'), expected_dict)

if __name__ == '__main__':
    unittest.main()
