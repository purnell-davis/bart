from app import app
from flask import render_template, flash, redirect
from forms import StationForm
import time

import bart

CURR_STATION = 'mont'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
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

'''
window.location = window.refresh()

window.location.hash 
"#dsfdsf"
f = window.location.hash
"#dsfdsf"
f.substr(1)
"dsfdsf"
'''
