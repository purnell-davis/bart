'''

'''
from flask.ext.wtf import Form
from wtforms import SelectField
from flask_app import bart

class StationForm(Form):
    '''
    
    '''
    station = SelectField('station', choices=sorted(bart.STATIONS.items()))
