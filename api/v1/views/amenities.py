#!/usr/bin/python3
"""
The api amenities module
"""
from flask import jsonify, abort, request

from api.v1.views import app_views, storage
from models import Amenity


@app_views.route('/amenities', methods=['GET'])
@app_views.route('/amenities/', methods=['GET'])
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenities(amenity_id=None):
    """
    Retrieve all amenities
    """
    if amenity_id:
        amenities = storage.get(cls=Amenity, id=amenity_id)
        if not amenities:
            abort(404)
        else:
            amenities = amenities.to_dict()
    else:
        amenities = storage.all(Amenity)
        amenities = [value.to_dict() for _, value in amenities.items()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenities(amenity_id=None):
    """
    Delete state linked to state_id
    """
    if amenity_id:
        state = storage.get(cls=Amenity, id=amenity_id)
        if state:
            storage.delete(obj=state)
            storage.save()
        else:
            abort(404)

    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    request_data = request.get_json()

    if not request_data:
        abort(400, "Not a JSON")

    if "name" not in request_data:
        abort(400, "Missing name")

    amenity = Amenity(name=request_data["name"])
    amenity.save()

    amenity_dict = amenity.to_dict()

    return jsonify(amenity_dict), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    request_data = request.get_json()

    if not request_data:
        abort(400, "Not a JSON")

    amenity = storage.get(cls=Amenity, id=amenity_id)
    if not amenity:
        abort(404)
    else:
        amenity_dict = amenity.to_dict()
        for key, value in request_data.items():
            amenity_dict[key] = value

        # delete old amenity
        storage.delete(obj=amenity)

        # Create a new amenity with new dict
        amenity = Amenity(**amenity_dict)

        # Save new amenity
        amenity.save()

        amenity_dict = amenity.to_dict()

    return jsonify(amenity_dict), 200
