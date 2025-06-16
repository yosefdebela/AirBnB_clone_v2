#!/usr/bin/python3
"""
Starts a Flask web application for AirBnB Clone V2 - Web Framework
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place

app = Flask(__name__)

# Close the SQLAlchemy session after each request
@app.teardown_appcontext
def teardown_db(exception):
    """Remove current SQLAlchemy session"""
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb_filters():
    """Displays a HTML page like 6-index.html with state, city, amenity, and place data"""
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    return render_template('100-hbnb.html',
                           states=states,
                           amenities=amenities,
                           places=places)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
