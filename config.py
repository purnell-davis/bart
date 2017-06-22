'''
Configuration for utilizing flask forms.
'''
import os

CSRF_ENABLED = True
SECRET_KEY = os.urandom(24)
