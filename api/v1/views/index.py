#!/usr/bin/python3
"""
Index Views
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage, Amenity, State, City, User, Review, \
    Place


@app_views.route('/status', methods=['GET'])
def status():
    status = {'status': 'OK'}
    return jsonify(status)


@app_views.route('/stats', methods=['GET'])
def get_stats():
    stats = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "states": storage.count(State),
        "users": storage.count(User),
        "reviews": storage.count(Review),
        "places": storage.count(Place)
    }

    return jsonify(stats)
