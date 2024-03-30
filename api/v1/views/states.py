#!/usr/bin/python3
"""
The api states module
"""
from api.v1.views import app_views, storage
from models import State
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'])
@app_views.route('/states/', methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'])
def get_states(state_id=None):
    """
    Retrieve all states
    """
    if state_id:
        states = storage.get(cls=State, id=state_id)
        if not states:
            abort(404)
        else:
            states = states.to_dict()
    else:
        states = storage.all(State)
        states = [value.to_dict() for _, value in states.items()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_states(state_id=None):
    """
    Delete state linked to state_id
    """
    if state_id:
        state = storage.get(cls=State, id=state_id)
        if state:
            storage.delete(obj=state)
            storage.save()
        else:
            abort(404)

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
@app_views.route('/states/', methods=['POST'])
def create_state():
    request_data = request.get_json()

    if not request_data:
        abort(400, "Not a JSON")

    if "name" not in request_data:
        abort(400, "Missing name")

    state = State(name=request_data["name"])
    state.save()

    state_dict = state.to_dict()

    return jsonify(state_dict), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    request_data = request.get_json()

    if not request_data:
        abort(400, "Not a JSON")

    state = storage.get(cls=State, id=state_id)
    if not state:
        abort(404)
    else:
        state_dict = state.to_dict()
        for key, value in request_data.items():
            state_dict[key] = value

        # delete old state
        storage.delete(obj=state)

        # Create a new state with new dict
        state = State(**state_dict)

        # Save new state
        state.save()

        state_dict = state.to_dict()

    return jsonify(state_dict), 200
