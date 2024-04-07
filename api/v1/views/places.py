#!/usr/bin/python3
"""
Places api module
"""

from flask import jsonify, request, abort
from api.v1.views import app_views, storage, Place, City, State


@app_views.route('/cities/<city_id>/places')
def get_places_by_city(city_id):
    """
    Retrieve all places associated with a city
    """
    if not city_id:
        abort(404)

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    places = city.places
    places_deserialized = [place.to_dict() for place in places]
    return jsonify(places_deserialized)


@app_views.route('/places/<place_id>', methods=["GET"])
def get_place_by_id(place_id):
    """
    Returns place using id

    Args:
        place_id: id of place to retrieve
    """

    place = storage.get(Place, place_id)

    if not place:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=["DELETE"])
def delete_place(place_id):
    """
    Delete place using id
    Args:
        place_id: id of place to delete
    """

    if not place_id:
        abort(404)

    place = storage.get(Place, place_id)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=["POST"])
def create_place(city_id):
    """
    Creates place using id of city

    Args:
        city_id: id of city to create place
    """

    if not city_id:
        abort(404)

    request_data = request.get_json()

    if not request_data:
        abort(400, "Not a JSON")

    if "user_id" not in request_data:
        abort(400, "Missing user_id")

    if "name" not in request_data:
        abort(400, "Missing name")

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    place_dict = {key: value for key, value in request_data.items()}
    place_dict["city_id"] = city_id

    place = Place(**place_dict)

    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=["PUT"])
def update_place(place_id):
    """
    Updates place using id
    Args:
        place_id: id of place to update
    """

    if not place_id:
        abort(404)

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    request_data = request.get_json()

    if not request_data:
        abort(400, "Not a JSON")

    place_dict = place.to_dict()

    for key, value in request_data.items():
        if key != "id" or \
                key != "user_id" or \
                key != "city_id" or \
                key != "created_at" or \
                key != "updated_at":
            place_dict[key] = value

    storage.delete(place)
    place = Place(**place_dict)
    place.save()

    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=["POST"])
def search_places():
    """Retrieves Place objects based on search criteria."""

    request_data = request.get_json()

    if not request_data:
        abort(400, "Not a JSON")

    states = request_data.get("states", [])
    cities = request_data.get("cities", [])
    amenities = request_data.get("amenities", [])

    # Retrieve all Place objects if no specific criteria are provided
    if not states and not cities and not amenities:
        places = storage.all(Place)
    elif states:
        # Get all cities in the specified states
        relevant_cities = set()
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                relevant_cities.update(city.id for city in state.cities)

        # Add individually specified cities, excluding those already in states
        relevant_cities.update(
            city for city in cities if city not in relevant_cities
        )

        # Retrieve places for the relevant cities
        places = [place for place in storage.all(Place) if place.city_id in relevant_cities]
    else:
        # Retrieve places for the specified cities
        places = [place for place in storage.all(Place) if place.city_id in cities]

    # Filter places by amenities if specified
    if amenities:
        places = [place for place in places if all(amenity in place.amenities for amenity in amenities)]

    return jsonify([place.to_dict() for place in places])

