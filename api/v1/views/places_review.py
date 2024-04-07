#!/usr/bin/python3
"""
Places Review api endpoints
"""

from flask import jsonify, request, abort

from api.v1.views import app_views, storage, Place, User, Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
    """
    Retrieves all reviews associated with a place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews = place.reviews
    reviews_list = [review.to_dict() for review in reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """
    Retrieves a specific review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Deletes a review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """
    Creates a new review
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")

    if "user_id" not in request_data:
        abort(400, "Missing user_id")

    if "text" not in request_data:
        abort(400, "Missing text")

    user = storage.get(User, request_data["user_id"])
    if not user:
        abort(404)

    review_dict = {key: value for key, value in request_data.items()}
    review_dict["place_id"] = place_id

    review = Review(**review_dict)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Updates a review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")

    for key, value in request_data.items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, key, value)

    storage.delete(review)
    review.save()
    return jsonify(review.to_dict()), 200
