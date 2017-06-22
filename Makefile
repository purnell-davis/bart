setup:
	virtualenv .venv

env:
	#Show information about environment
	which python
	python --version
	which nosetests
	which pylint

lint:
	pylint --load-plugins pylint_flask --disable=R,C flask_app/*.py flask_app/models/*.py

test:
	nosetests --with-cov flask_app/tests/*

install:
	pip install -r requirements.txt 

start-api:
	python run.py

all: install lint test
