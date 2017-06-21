# netflix
Interview Question For Netflix

## How to run example and setup environment:

To create environment (tested on OS X 10.12.5), run `make setup`, which does the following commands below:

```
mkdir -p ~/.nflixenv && python3 -m venv ~/.nflixenv
```

Then source the virtualenv.  Typically I do it this way, I add an alias to my .zshrc:

```
alias ntop="cd ~/src/netflix && source ~/.nflixenv/bin/activate"
```

I can then type in:  `ntop` and I cd into my checkout and source a virtualenv.  Next, I then make sure I have the latest packages and that linting and tests pass by running make all:

```make all```


I also like to verify that pylint and pytest and python are exactly the versions I expect, so I added a make command env to conveniently check for these:

```make env

(.nflixenv) ➜  netflix git:(master) ✗ make env
#Show information about environment
which python3
/Users/noahgift/.nflixenv/bin/python3
python3 --version
Python 3.6.1
which pytest
/Users/noahgift/.nflixenv/bin/pytest
which pylint
/Users/noahgift/.nflixenv/bin/pylint
```

## How to interact with Commandline tool (Click Framework):


Check Version:

```
(.nflixenv) ➜  netflix git:(master) ✗ ./csvutil.py --version
csvutil.py, version 0.1
```

Check Help:

```
(.nflixenv) ➜  netflix git:(master) ✗ ./csvutil.py --help   
Usage: csvutil.py [OPTIONS] COMMAND [ARGS]...

  CSV Operations Tool



Options:
  --version  Show the version and exit.
  --help     Show this message and exit.
```

## How to run webapp (primary question) and use API

To run the flask api (if you have followed instructions above), you should be able to run the make command `make start-api`.  The output should look like this:

```
(.nflixenv) ➜  netflix git:(master) ✗ make start-api
#sets PYTHONPATH to directory above, would do differently in production
cd flask_app && PYTHONPATH=".." python web.py
2017-06-17 16:34:15,049 - __main__ - INFO - START Flask
 * Running on http://0.0.0.0:5001/ (Press CTRL+C to quit)
 * Restarting with stat
2017-06-17 16:34:15,473 - __main__ - INFO - START Flask
 * Debugger is active!
 * Debugger PIN: 122-568-160
2017-06-17 16:34:43,736 - __main__ - INFO - {'/api/help': 'Print available api routes', '/favicon.ico': 'The Favicon', '/': 'Home Page'}
127.0.0.1 - - [17/Jun/2017 16:34:43] "GET / HTTP/1.1" 200 -
```

Next, open a web browser to view API documentation (formatted as HTML):

http://0.0.0.0:5001/

To query the api from the commandline, I would highly recommend httpie:  https://httpie.org/.  To query all available api endpoints and get JSON result.  Here is what the output should look like:

```
(.nflixenv) ➜  netflix git:(master) ✗ http GET http://0.0.0.0:5001/api/help 
HTTP/1.0 200 OK
Content-Length: 106
Content-Type: application/json
Date: Sat, 17 Jun 2017 23:46:08 GMT
Server: Werkzeug/0.12.2 Python/3.6.1

{
    "/": "Home Page",
    "/api/help": "Return all API Routes as JSON",
    "/favicon.ico": "The Favicon"
}
```

Alternately, using the requests library you can query the api as follows in IPython:

```

import requests
In [1]: url = "http://0.0.0.0:5001/api/csv/aggregate/last_name"
In [2]: with open("ext/input.csv", "rb") as f:
    ...:     data = base64.b64encode(f.read())

In [3]: r = requests.post(url, data=data)

In [4]: r.content
Out[4]: b'{"count":{"eagle":34,"lee":3,"smith":27}}'

## How to interact with library:

Typically I use commandline IPython to test libraries that I create.  Here is how to ensure the library is working (should be able to get version number):

```
In [1]: from nlib import csvops

In [2]: df = csvops.ingest_csv("ext/input.csv")
2017-06-17 17:00:33,973 - nlib.csvops - INFO - CSV to DF conversion with CSV File Path ext/input.csv

In [3]: df.head()
Out[3]: 
  first_name last_name  count
0      piers     smith     10
1    kristen     smith     17
2       john       lee      3
3        sam     eagle     15
4       john     eagle     19

```

## Answers to THINGS TO THINK ABOUT

1. Think about the interface to the api.  While the sample input and output indicate csv (including the aggregation) give an interface that is straight forward to use.
2. How easy is it to change the implementation to do other (or arbitrary aggregations)?
3. If we wanted to start pulling the data from another source, how would you change your implementation?
4. If we wanted to hold the data in memory and perform aggregations how would that affect the design?  And the scaling?
5. At what point would you consider not writing this simple service and look at other solutions to the same problem?  What would you consider instead?
