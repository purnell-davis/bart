'''
Form data.
This app contains a dropdown menu, listing the BART stations.
'''
from flask_wtf import Form
from wtforms import SelectField
from flask_app.models import bart

class StationForm(Form):
    '''
    Form that contains a dropdown menu containing a list of BART stations.
    '''
    stations = sorted([station['station_name'] for station in bart.stations()])
    station = SelectField('station', choices=stations)
