#!/usr/bin/python3
"""
Cities API
"""

from flask import jsonify, request, abort
from api.v1.views import app_views, storage
from models import State, City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id):
    """
    Get all cities of a state
    """
    if not state_id:
        abort(404)
    else:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        cities = state.cities
        cities = [city.to_dict() for city in cities]

    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """
    Get a city by id
    """
    if not city_id:
        abort(404)

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    city_dict = city.to_dict()

    return jsonify(city_dict)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """
    Delete a city by id
    """
    if not city_id:
        abort(404)

    city = storage.get(City, city_id)

    if not city:
        abort(404)
    else:
        storage.delete(city)
        storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """
    Create a new city

    Args:
        state_id (string): The id of the state

    Returns:
        (string): The json response
    """

    if not state_id:
        abort(404)
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    request_data = request.get_json()

    if not request_data:
        abort(400, "Not a JSON")

    if "name" not in request_data:
        abort(400, "Missing name")

    city = City(name=request_data["name"], state_id=state_id)
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """
    Update a city by id
    Args:
        city_id (string): The id of the city to update
    """

    if not city_id:
        abort(404)

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    request_data = request.get_json()

    if not request_data:
        abort(400, "Not a JSON")

    if "name" not in request_data:
        abort(400, "Missing name")

    city_dict = city.to_dict()

    for key, value in request_data.items():
        city_dict[key] = value

    # delete the old city
    storage.delete(city)

    new_city = City(**city_dict)
    new_city.save()

    return jsonify(city_dict), 201
