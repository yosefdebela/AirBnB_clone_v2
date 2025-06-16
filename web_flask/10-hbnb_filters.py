#!/usr/bin/python3
"""
Flask web application with filtering of Places by amenities, states, and cities
"""

from flask import Flask, render_template, request
from models import storage
from models.state import State
from models.place import Place
from models.amenity import Amenity

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception=None):
    """Remove SQLAlchemy session on teardown."""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """
    Render the hbnb filters page with:
    - A list of all amenities
    - A list of all states (each containing its cities)
    - Places filtered based on selected amenity/state/city
    """
    # Retrieve all amenities, states (with cities), and initial places
    amenities = storage.all(Amenity).values()
    states = storage.all(State).values()
    places = storage.all(Place).values()

    # Retrieve filters from query parameters (form submission)
    amenity_ids = request.args.getlist('amenities')
    state_ids = request.args.getlist('states')
    city_ids = request.args.getlist('cities')

    if amenity_ids or state_ids or city_ids:
        filtered = []
        for place in places:
            if amenity_ids:
                # Check if place has all selected amenities
                if not all(any(amenity.id == aid for amenity in place.amenities)
                           for aid in amenity_ids):
                    continue

            if city_ids:
                if place.city_id not in city_ids:
                    continue
            elif state_ids:
                # If no city filter but state(s), ensure place.city belongs to selected states
                if place.city.state_id not in state_ids:
                    continue

            filtered.append(place)
        places = filtered

    return render_template('10-hbnb_filters.html',
                           amenities=amenities,
                           states=states,
                           places=places)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
