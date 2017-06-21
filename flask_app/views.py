'''
The View/Controller for this app.
Displays the real time bart schedule for a particular station.
'''
import time
from flask_app import app
from flask_app.forms import StationForm
from flask import render_template

from flask_app.models import bart

CURR_STATION = 'mont'

#@TODO: sep validation logic
    #@TODO: sep data logic
    #@TODO: views/routes
    #@TODO: controller

    # get input, validate, get data, display data

#@TODO: logging
app.logger.debug('A value for debugging')


#@TODO: route to stations
@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    
    '''
    station_form = StationForm()

    global CURR_STATION
    if station_form.validate_on_submit():
        station = station_form.station.data
        CURR_STATION = station
        #return redirect('/index#%s' % (station))
    else:
        station = CURR_STATION

    schedule = bart.schedule(station)
    destinations = {}
    for destination in schedule['destinations']:
        destinations.setdefault(
            destination['direction'], []).append(destination)

    return render_template("index.html",
                           title='BART',
                           curr_time=time.strftime('%I:%M:%S %p'),
                           station_form=station_form,
                           station=schedule['station_name'],
                           destinations=destinations)

#@TODO: json route
#@TODO: stations json
