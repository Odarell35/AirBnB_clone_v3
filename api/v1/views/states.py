#!/usr/bin/python3
"""
List all states
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.state import State
from models import storage

@app_views.route("/states", strict_slashes=False, methods=["GET"] )
def get_all_state():
        """
        get all instance
        """
        states_list = []
        states = storage.all(State).values()
        for state_obj in states:
            states_list.append(state_obj.to_dict())
        return jsonify(states_list)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"] )
def get_state(state_id):
    """get specific state"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["DELETE"] )
def del_state(state_id):
    """DELETE STATE"""
    state = storage.get(State, state_id)
    if state:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    """creates state"""
    json_data = request.get_json()
    if json_data:
        new = State(**json_data)
        new.save()
        return jsonify(new.to_dict()), 201
    else:
        abort(400, "Not a JSON")
    if "name" not in json_data:
        abort(400, "Missing name")


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    """updates instance"""
    json_data = request.get_json()
    if not json_data:
        abort(400, "Not a JSON")
    prev_state = storage.get(State, state_id)
    if prev_state:
        prev_state.name = json_data.get("name", prev_state.name)
        prev_state.save()
        return jsonify(prev_state.to_dict()), 200
    else:
        abort (404)
