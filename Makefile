setup:
	virtualenv .venv

env:
	#Show information about environment
	which python
	python --version
	which nosetests
	which pylint

lint:
	pylint --load-plugins pylint_flask --disable=R,C flask_app/*.py

test:
	nosetests --with-cov

install:
	pip install -r requirements.txt 

start-api:
	#sets PYTHONPATH to directory above, would do differently in production
	python run.py

all: install lint test
