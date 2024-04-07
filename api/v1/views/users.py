#!/usr/bin/python3
"""
User api module
"""

from flask import request, jsonify, abort

from api.v1.views import app_views, storage
from models import User


@app_views.route('/users', methods=['GET'])
@app_views.route('/users/', methods=['GET'])
def get_users():
    """
    Get all users
    """
    users = storage.all(User)
    users_dict = [user.to_dict() for _, user in users.items()]

    return jsonify(users_dict)


@app_views.route('/users/<user_id>', methods=["GET"])
def get_user(user_id):
    """
    Get user details
    Args:
        user_id: user id

    Returns:
        user: user details
    """

    if not user_id:
        abort(404)

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=["DELETE"])
def delete_user(user_id):
    """
    Delete user details

    Args:
        user_id: user id

    Returns:
        json: empty
        code: 200
    """

    if not user_id:
        abort(404)

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """
    Create new user

    Returns:
        user: user details
    """

    request_json = request.get_json()

    if not request_json:
        abort(400, "Not a JSON")

    if "email" not in request_json:
        abort(400, "Missing email")

    if "password" not in request_json:
        abort(400, "Missing password")

    user = User(**request_json)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update user details

    Args:
        user_id: user id

    Returns:
        user: user details
        code: status code
    """
    if not request.json:
        abort(400, "Not a JSON")

    if not user_id:
        abort(400, "Missing id")

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    user_dict = user.to_dict()

    for key, value in request.json.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            user_dict[key] = value

    # update user attributes
    for key, value in user_dict.items():
        setattr(user, key, value)

    user.save()

    return jsonify(user.to_dict()), 200
