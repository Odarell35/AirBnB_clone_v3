#!/usr/bin/python3
"""City objects that hand;e api actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import abort, request, jsonify


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                methods=['GET'])
def city_objs(state_id):
    """Retrieves the list of all City objects of a State
    """
    #looks for states with given id
    list_city = []
    state_obj = storage.get(State, state_id)
    if state_obj:
        #retrieve all the city within the found state
        city_objs = state_obj.cities
        for city in city_objs:
            list_city.append(city.to_dict())
        return jsonify(list_city)
    else:
        abort (404)


@app_views.route("/cities/<city_id>", strict_slashes=False,
                methods=["GET"])
def get_city_obj(city_id):
    """Retrieves a City object"""
    obj = storage.get(City, city_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", strict_slashes=False, methods=["POST"])
def creates_city(state_id):
    """creates city with given state_id"""
    json_data = request.get_json()
    if not json_data:
        abort(400, "Not a JSON")
    if "name" not in json_data:
        abort(400, "Missing name")
    state = storage.get(State, state_id)
    if state:
        json_data['state_id'] = state_id
        new_city = City(**json_data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201
    else:
        abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def updates_city(city_id):
    """updates"""
    json_data = request.get_json()
    if not json_data:
        abort(400, "Not a JSON")
    prev_city = storage.get(City, city_id)
    if prev_city:
        prev_city.name = json_data.get("name", prev_city.name)
        prev_city.save()
        return jsonify(prev_city.to_dict()), 200
    else:
        abort (404)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def del_city(city_id):
    """deletes """
    city = storage.get(City, city_id)
    if city:
            storage.delete(city)
            storage.save()
            return jsonify({}), 200
    else:
        abort(404)
