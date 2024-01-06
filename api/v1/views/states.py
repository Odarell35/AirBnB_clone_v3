#!/usr/bin/python3
"""
List all states
"""
from flask import jsonify, request
from flask.views import MethodView
from models import State  # Make sure to import your State model


class StatesAPI(MethodView):
    def get(self, state_id=None):
        """
        get instance
        """
        if state_id is None:
            states = State.query.all()
            states_list = [state.to_dict() for state in states]
            return jsonify(states_list)
        else:
            state = State.query.get(state_id)
            if state:
                return jsonify(state.to_dict())
            else:
                return jsonify({"error": "State not found"}), 404

    def post(self):
        """
        post state
        """
        data = request.get_json()
        new_state = State(**data)
        new_state.save()  # Assuming there is a save method in your State model
        return jsonify(new_state.to_dict()), 201

    def put(self, state_id):
        """
        update a specific state by ID
        """
        state = State.query.get(state_id)
        if state:
            data = request.get_json()
            state.update(data)  # Assuming there is an update method in your State model
            return jsonify(state.to_dict())
        else:
            return jsonify({"error": "State not found"}), 404

    def delete(self, state_id):
        '''Delete a specific state by ID'''
        state = State.query.get(state_id)
        if state:
            state.delete()  # Assuming there is a delete method in your State model
            return jsonify({"message": "State deleted successfully"})
        else:
            return jsonify({"error": "State not found"}), 404
