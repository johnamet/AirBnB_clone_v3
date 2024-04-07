#!/usr/bin/python3
"""
Places Amenities api endpoints
"""


from flask import jsonify, abort
from models import Place, Amenity, storage_t
from api.v1.views import app_views, storage


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities_by_place(place_id):
    """
    Retrieves all amenities associated with a place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    # Handle based on storage type
    if storage_t == "db":
        amenities = storage.all(Amenity).values()
        place_amenities = [amenity for amenity in amenities if amenity.place_id == place_id]
    else:
        place_amenities = [amenity for amenity in place.amenity_ids if storage.get(Amenity, amenity)]

    amenities_list = [amenity.to_dict() for amenity in place_amenities]
    return jsonify(amenities_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity_from_place(place_id, amenity_id):
    """
    Deletes a link between a place and an amenity
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if storage_t == "db":
        if amenity.place_id != place_id:
            abort(404)
        amenity.place_id = None
        storage.save(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
        storage.save(place)

    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    """
    Links an amenity to a place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if storage_t == "db":
        if amenity.place_id is not None:
            return jsonify(amenity.to_dict()), 200
        amenity.place_id = place_id
        storage.save(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
        storage.save(place)

    return jsonify(amenity.to_dict()), 201
