#!/usr/bin/python3
"""
The api states module
"""
from flask import jsonify, abort, request

from api.v1.views import app_views, storage
from models import State


@app_views.route('/states', methods=['GET'])
@app_views.route('/states/', methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'])
def get_states(state_id=None):
    """
    Retrieve all states or a specific state by id
    """
    if state_id:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        return jsonify(state.to_dict()), 200
    else:
        states = storage.all(State).values()
        return jsonify([state.to_dict() for state in states]), 200


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id=None):
    """
    Delete state by id
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
@app_views.route('/states/', methods=['POST'])
def create_state():
    """
    Create a new state
    """
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    if "name" not in request_data:
        abort(400, "Missing name")
    new_state = State(**request_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """
    Update state by id
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200