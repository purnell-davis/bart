#!/usr/bin/python
'''
Python API for using bart REST API.
'''
import xml.etree.ElementTree as ET
import requests

KEY = "MW9S-E7SL-26DU-VV8V"

#@TODO: change to use api call
STATIONS = {
"12th": "12th St. Oakland City Center",
"16th": "16th St. Mission (SF)",
"19th": "19th St. Oakland",
"24th": "24th St. Mission (SF)",
"ashb": "Ashby (Berkeley)",
"balb": "Balboa Park (SF)",
"bayf": "Bay Fair (San Leandro)",
"cast": "Castro Valley",
"civc": "Civic Center (SF)",
"cols": "Coliseum/Oakland Airport",
"colm": "Colma",
"conc": "Concord",
"daly": "Daly City",
"dbrk": "Downtown Berkeley",
"dubl": "Dublin/Pleasanton",
"deln": "El Cerrito del Norte",
"plza": "El Cerrito Plaza",
"embr": "Embarcadero (SF)",
"frmt": "Fremont",
"ftvl": "Fruitvale (Oakland)",
"glen": "Glen Park (SF)",
"hayw": "Hayward",
"lafy": "Lafayette",
"lake": "Lake Merritt (Oakland)",
"mcar": "MacArthur (Oakland)",
"mlbr": "Millbrae",
"mont": "Montgomery St. (SF)",
"nbrk": "North Berkeley",
"ncon": "North Concord/Martinez",
"orin": "Orinda",
"pitt": "Pittsburg/Bay Point",
"phil": "Pleasant Hill",
"powl": "Powell St. (SF)",
"rich": "Richmond",
"rock": "Rockridge (Oakland)",
"sbrn": "San Bruno",
"sfia": "San Francisco Int'l Airport",
"sanl": "San Leandro",
"shay": "South Hayward",
"ssan": "South San Francisco",
"ucty": "Union City",
"wcrk": "Walnut Creek",
"wdub": "West Dublin",
"woak": "West Oakland",
}

def schedule(station):
    '''
    Use the BART REST API to deduce the given station's schedule.
    '''
    bart_rest_url = 'http://api.bart.gov/api/etd.aspx?cmd=etd&orig=%s&key=%s' \
      % (station, KEY)
    req = requests.get(bart_rest_url)
    root = ET.fromstring(req.text)

    # get root info
    schedule_data = {}
    schedule_data['station_name'] = root.find('./station/name').text
    schedule_data['station_abbr'] = root.find('./station/abbr').text

    # get station etd info
    schedule_data['destinations'] = []
    for etd in root.findall('./station/etd'):
        # get destination info
        destination_dict = {}
        destination_dict['destination_name'] = etd.find('destination').text
        destination_dict['destination_abbr'] = etd.find('abbreviation').text
        destination_dict['estimates'] = []

        # get estimate info
        for estimate in etd.findall('estimate'):
            estimate_dict = {}
            estimate_dict['minutes'] = estimate.find('minutes').text
            estimate_dict['length'] = estimate.find('length').text

            destination_dict.setdefault(
              'color', estimate.find('color').text)
            destination_dict.setdefault(
              'hexcolor', estimate.find('hexcolor').text)
            destination_dict.setdefault(
              'direction', estimate.find('direction').text)

            destination_dict['estimates'].append(estimate_dict)

        schedule_data['destinations'].append(destination_dict)

    return schedule_data

