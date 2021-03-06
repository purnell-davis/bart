'''
Forms.

This app contains a dropdown menu, listing the BART stations.
'''
from flask_wtf import FlaskForm
from wtforms import SelectField
from flask_app.models import bart

class StationForm(FlaskForm):
    '''
    Form that contains a dropdown menu containing a list of BART stations.
    '''
    stations = [(station['station_abbr'], station['station_name']) \
        for station in bart.stations()]

    station = SelectField('station', choices=sorted(stations))
