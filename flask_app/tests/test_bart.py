#!/usr/bin/python
'''
Functional test, testing the functionality of bart.py.
'''

import unittest
from flask_app.models import bart
from mock import patch
from mock import MagicMock

ETD_XML = \
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

ERROR_XML = \
'''<?xml version="1.0" encoding="utf-8"?>
<root>
    <message>
        <error>
            <text>Invalid orig</text>
            <details>The orig station parameter ETA is missing or invalid.</details>
        </error>
    </message>
</root>
'''

class Test_schedule(unittest.TestCase):

    @patch('flask_app.models.bart.BartRestApi.etd')
    def test_dict_is_correct(self, api_etd_mock):
        api_etd_mock.return_value = ETD_XML
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

    @patch('flask_app.models.bart.BartRestApi.etd')
    def test_error_caught_correctly(self, api_etd_mock):
        api_etd_mock.return_value = ERROR_XML

        details_msg = 'The orig station parameter ETA is missing or invalid.'
        expected_dict = {'errors': [{'text': 'Invalid orig',
                                     'details': details_msg}]}

        self.assertEquals(bart.schedule('rich'), expected_dict)

STATION_XML = \
'''<root>
    <uri>
        <![CDATA[ http://api.bart.gov/api/stn.aspx?cmd=stns ]]>
    </uri>
    <stations>
        <station>
            <name>12th St. Oakland City Center</name>
            <abbr>12TH</abbr>
            <gtfs_latitude>37.803768</gtfs_latitude>
            <gtfs_longitude>-122.271450</gtfs_longitude>
            <address>1245 Broadway</address>
            <city>Oakland</city>
            <county>alameda</county>
            <state>CA</state>
            <zipcode>94612</zipcode>
        </station>
        <station>
            <name>16th St. Mission</name>
            <abbr>16TH</abbr>
            <gtfs_latitude>37.765062</gtfs_latitude>
            <gtfs_longitude>-122.419694</gtfs_longitude>
            <address>2000 Mission Street</address>
            <city>San Francisco</city>
            <county>sanfrancisco</county>
            <state>CA</state>
            <zipcode>94110</zipcode>
        </station>
    </stations>
    <message/>
</root>'''

class Test_stations(unittest.TestCase):

    @patch('flask_app.models.bart.BartRestApi.stations')
    def test_dict_is_correct(self, api_station_mock):
        api_station_mock.return_value = STATION_XML

        expected_dict = [{'station_name': '12th St. Oakland City Center',
                          'station_abbr': '12TH'},
                         {'station_name': '16th St. Mission',
                          'station_abbr': '16TH'}
                        ]

        self.assertEquals(bart.stations(), expected_dict)

    
if __name__ == '__main__':
    unittest.main()
