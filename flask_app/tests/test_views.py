#!/usr/bin/python
'''
Unittest, testing the functionality of views.py.
'''

import json
import unittest
from flask_app import views, app

class Test_reformat_destinations_for_view(unittest.TestCase):

    def test_correct_destinations_dict(self):
        destinations = [{'destination_name': 'Daly City',
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
                            'length': '6'}]},
                        {'destination_name': 'Fremontz',
                         'destination_abbr': 'FRMT',
                         'direction': 'North',
                         'color': 'ORANGE',
                         'hexcolor': '#ff9933',
                         'estimates': [
                           {'minutes': '17', 
                            'length': '6'},
                           {'minutes': '37', 
                            'length': '6'}]}]

        reformatted_dests = views._reformat_destinations_for_view(destinations)

        expected_result = {'South': [{'destination_name': 'Daly City',
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
                                         'length': '6'}]}],
                           'North': [{'destination_name': 'Fremontz',
                                      'destination_abbr': 'FRMT',
                                      'direction': 'North',
                                      'color': 'ORANGE',
                                      'hexcolor': '#ff9933',
                                      'estimates': [
                                        {'minutes': '17', 
                                         'length': '6'},
                                        {'minutes': '37', 
                                         'length': '6'}]}]}

        self.assertEquals(reformatted_dests, expected_result)


class Test_api_helper(unittest.TestCase):

    def test_index_in_destinations(self):
        funcs = views._api_helper()
        self.assertTrue(funcs.has_key('/'))

    def test_eta_in_destinations(self):
        funcs = views._api_helper()
        self.assertTrue(funcs.has_key('/eta'))

    def test_stations_in_destinations(self):
        funcs = views._api_helper()
        self.assertTrue(funcs.has_key('/stations'))

    def test_eta_station_in_destinations(self):
        funcs = views._api_helper()
        self.assertTrue(funcs.has_key('/eta/<station>'))

    def test_favicon_in_destinations(self):
        funcs = views._api_helper()
        self.assertTrue(funcs.has_key('/favicon.ico'))


class Test_stations_route(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_returns_list_of_stations(self):
        result = self.app.get('/stations')
        result_data = json.loads(result.data)
        self.assertTrue(result_data)
        for station in result_data:
            self.assertTrue(station.has_key('station_name'))
            self.assertTrue(station.has_key('station_abbr'))


class Test_eta_station_route(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_returns_list_of_stations(self):
        fake_station = 'FAKE_STATION'
        result = self.app.get('/eta/%s' % (fake_station))
        result_data = json.loads(result.data)

        expected_result = {
            'errors': [{'text': 'Invalid orig',
                        'details': 'The orig station parameter %s is missing or invalid.' % (fake_station)}]}

        self.assertEquals(expected_result, result_data)
        self.assertEquals(result.status_code, 404)

if __name__ == '__main__':
    unittest.main()
