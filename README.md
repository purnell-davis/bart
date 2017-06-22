# BART ETA
Displays BART ETA for trains at specified stations.

## How to run example and setup environment:

Tested against Python 2.7.10 on OSX 10.12.5

Sets up a virtual environment to install packages for testing.

First, create the environment. Call `make setup`, which runs:

```
virtualenv .venv
```

If virtualenv not installed do:

```
pip install virtualenv
```

```
source .venv/bin/activate"
```

Then make sure the latest packages are installed and that linting and tests pass:

```
make all
```


You can verify that pylint, nosetests and python are the expected versions:

```
make env
```

## How to run the webapp and use the REST API

To run the flask api, run `make start-api`.  The output should look like this:

```
python run.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 513-965-567
```

Next, open a web browser to view some API documentation:

http://0.0.0.0:5000/

The main functionality exists under `eta/<station>` where station is an abbreviated string for a particular bart station.

You can see those names listed under `eta/` or `stations/`.

The app displays each incoming train for the given station.  It shows the time it will take to get to the station and the length of the train. It also contains a dropdown form to allow you to choose other stations if you'd like.

I used this at work whenever I was about to leave and I wanted to time my walk to the bart station.

## Feature idea

One thing I wanted to add was alerts that I could set, based on the distance from the office to the station.  It would tell me exactly when to leave the office to catch the next train.

Another idea is to add a json route to each station to view the json.  It could be helpful to others, because the official BART api returns XML.

I'd also love to style it more (CSS and JavaScript).
