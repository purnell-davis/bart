#!/usr/bin/python
'''
Python API for using bart REST API.
'''
from flask_app import app
import xml.etree.ElementTree as ET
import requests

class BartRestApi(object):
    '''
    Class to organize BART REST API calls.
    '''
    # https://www.bart.gov/schedules/developers/api
    key = "MW9S-E7SL-26DU-VV8V"

    @classmethod
    def etd(cls, station):
        '''
        Calls the etd BART API REST endpoint.

        PARAM station str
            Station to pull the schedule for.

        RETURN str
            XML string data of the etd schedule.
        '''
        # https://api.bart.gov/docs/etd/etd.aspx
        etd_url = 'http://api.bart.gov/api/etd.aspx?cmd=etd&orig=%s&key=%s' \
          % (station, cls.key)

        app.logger.debug('GET %s', etd_url)
        req = requests.get(etd_url)

        return req.text

    @classmethod
    def stations(cls):
        '''
        Calls the etd BART API REST endpoint.

        RETURN str
            XML string data of the stations.
        '''
        # https://api.bart.gov/docs/stn/stns.aspx
        stns_url = 'http://api.bart.gov/api/stn.aspx?cmd=stns&key=%s' \
          % (cls.key)

        app.logger.debug('GET %s', stns_url)
        req = requests.get(stns_url)

        return req.text

def _etd(estimate):
    '''
    Parse the XML estimate block and convert to dictionary.
    Data pertains to the etd and length of next train.

    Attributes:
        minutes
        length

    PARAM estimate xml.etree.Element
        Object representing the XML estimate block.

    RETURN dict
        Data pertaining to the estimated time and length of next train.
    '''
    estimate_dict = {}
    estimate_dict['minutes'] = estimate.find('minutes').text
    estimate_dict['length'] = estimate.find('length').text

    return estimate_dict

def _station_destination(destination_station):
    '''
    Parse the XML etd block and convert to dictionary.
    Data pertains to the destination station.

    Attributes:
        destination_name
        destination_abbr
        color
        hexcolor
        direction
        estimates

    PARAM destination_station xml.etree.Element
        Object representing the XML etd block.

    RETURN dict
        Data pertaining to the destination station.
    '''
    # get destination info
    destination_dict = {}
    destination_dict['destination_name'] = \
        destination_station.find('destination').text
    destination_dict['destination_abbr'] = \
      destination_station.find('abbreviation').text

    destination_dict['estimates'] = []
    for estimate in destination_station.findall('estimate'):
        destination_dict['estimates'].append(_etd(estimate))

        # set some etd data on the destination level
        destination_dict.setdefault('color', estimate.find('color').text)
        destination_dict.setdefault('hexcolor', estimate.find('hexcolor').text)
        destination_dict.setdefault(
            'direction', estimate.find('direction').text)


    return destination_dict

def schedule(station):
    '''
    Use the BART REST API to retrieve the given station's schedule.
    Convert from XML into a dictionary.

    Attributes:
        station_name
        station_abbreviation
        station_destinations

    PARAM station str
        Name of the station whose schedule we want to view.

    RETURN dict
        Schedule data
    '''
    root = ET.fromstring(BartRestApi.etd(station))

    # error checking
    if root.find('./message/error') is not None:
        return {'errors':
                    [{'text': root.find('./message/error/text').text,
                      'details': root.find('./message/error/details').text}]}

    # get root info
    schedule_data = {}
    schedule_data['station_name'] = root.find('./station/name').text
    schedule_data['station_abbr'] = root.find('./station/abbr').text

    # get station etd info
    schedule_data['destinations'] = [
        _station_destination(etd) for etd in root.findall('./station/etd')]

    return schedule_data


def stations():
    '''
    Use the BART REST API to retrieve a list of stations.
    Convert from XML into a list.

    Attributes:
        station_name
        station_abbreviation

    RETURN list
        List of BART stations.
    '''
    root = ET.fromstring(BartRestApi.stations())

    station_data = []
    for station in root.findall('./stations/station'):
        station_data.append({'station_name': station.find('name').text,
                             'station_abbr': station.find('abbr').text})

    return station_data
