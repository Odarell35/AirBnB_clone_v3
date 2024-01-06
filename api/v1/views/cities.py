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
        return {
                "ERROR"
                }
