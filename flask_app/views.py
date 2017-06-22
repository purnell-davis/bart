'''
The View/Controller for this app.
Displays the real time bart schedule for a particular station.
'''
import os
import time
from flask_app import app
from flask_app.forms import StationForm
from flask_app.models import bart

from flask import render_template, jsonify, redirect, url_for, \
                  send_from_directory

@app.route('/favicon.ico')
def favicon():
    '''
    favicon for the browser.
    '''
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')

def _reformat_destinations_for_view(destinations):
    '''
    Reformats the destinations for injestion into the view template.
    Sets the direction as a top level attribute for each destination train.

    PARAM destinations dict
        Destination info to reformat for the view.

    RETURN dict
        Dictionary of destinations reformatted.
    '''
    reformatted_destinations = {}

    # organize each destination within the station direction
    for destination in destinations:
        reformatted_destinations.setdefault(
            destination['direction'], []).append(destination)

    return reformatted_destinations

@app.route('/eta/<station>', methods=['GET', 'POST'])
def eta(station):
    '''
    The view displays the BART real time eta's for trains at a given station.
    Contains a form which lists the BART stations that can be selected.

    PARAM station str
        Station to display eta info for.
    '''
    station_form = StationForm()

    # manage the form input
    if station_form.validate_on_submit():
        return redirect(url_for('eta', station=station_form.station.data))

    app.logger.debug('Retrieve station schedule')
    schedule = bart.schedule(station)
    app.logger.info('Retrieved schedule: %s', schedule)

    # error handling, return 404
    if schedule.get('errors'):
        resp = jsonify(schedule)
        resp.status_code = 404
        app.logger.error(schedule)

        return resp

    return render_template("eta.html",
                           title='BART ETA (%s)' % (station),
                           curr_time=time.strftime('%I:%M:%S %p'),
                           station_form=station_form,
                           station=schedule['station_name'],
                           destinations=_reformat_destinations_for_view(
                               schedule['destinations']))

@app.route('/eta', methods=['GET', 'POST'])
def eta_stations():
    '''
    Present a list of stations and their respective hyperlinks/routes.
    '''
    stations_list = bart.stations()
    app.logger.info(stations_list)

    return render_template("eta_stations.html", stations=stations_list)

def _api_helper():
    '''
    Helper method to parse app url map

    RETURN dict
        Route functions and their docstrings.
    '''
    funcs = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            funcs[rule.rule] = app.view_functions[rule.endpoint].__doc__

    return funcs

@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    Index for the app.
    The view displays the endpoints that can be used.
    '''
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__

    app.logger.info(func_list)

    return render_template("index.html", routes=func_list)

@app.route('/stations', methods=['GET'])
def stations():
    '''
    Lists the available stations to select.
    '''
    stations_list = bart.stations()
    app.logger.info(stations_list)

    return jsonify(stations_list)
