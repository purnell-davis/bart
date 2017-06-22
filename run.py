#!.venv/bin/python
'''
Starting point for running the flask app.
'''
from flask_app import app

#app.run('0.0.0.0', debug = True)
app.run(debug=True)
