#!/usr/bin/python3
"""Importing Flask to run the web app"""
from flask import Flask, render_template
from models import storage

# HBNB_MYSQL_USER='hbnb_dev'
# HBNB_MYSQL_PWD='hbnb_dev_pwd'
# HBNB_MYSQL_HOST='localhost'
# HBNB_MYSQL_DB='hbnb_dev_db'
# HBNB_TYPE_STORAGE='db'

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def display_states():
    """Render state_list html page to display States created"""
    states = storage.all()
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(self):
    """Method to remove current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
