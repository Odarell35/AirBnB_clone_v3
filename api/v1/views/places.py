#!/usr/bin/python3
"""
Place objects that handles all default RESTFul API actions
"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("cities/<city_id>/places", strict_slashes=False,
                 methods=['GET'])
def get_place(city_id=None):
    """
    Returns list of Place objects linked to any City
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    cities = []
    for item in city.places:
        cities.append(item.to_dict())
    return jsonify(cities)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=['GET'])
def get_place_id(place_id):
    '''
    Get the Place by place id
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id=None):
    """
    Delete Place from database
    """
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    places.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['POST'])
def post_place(city_id):
    """
    fetches and post a Place in city
    """
    if storage.get(City, city_id) is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")
    if storage.get(User, request.get_json()["user_id"]) is None:
        abort(404)
    if "name" not in request.get_json():
        abort(400, "Missing name")
    places = Place(**request.get_json())
    places.city_id = city_id
    places.save()
    return jsonify(places.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["PUT"])
def update_place(place_id=None):
    """ Update user objects
    """
    key = "Place." + str(place_id)
    if key not in storage.all(Place).keys():
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    place = storage.get(Place, place_id)
    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
