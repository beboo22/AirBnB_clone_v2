#!/usr/bin/python3
"""
Starts a Flask web application
"""

from flask import Flask, render_template
from models import *
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardwn():
    """closes the storage on teardown"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """display a HTML page with the states listed in alphabetical order"""
    hone = 'States'
    states = storage.all("State").values()
    return render_template('8-cities_by_states.html', hone=hone, states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
