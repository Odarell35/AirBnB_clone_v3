#!/usr/bin/python3
"""Amenity objects that handle api actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from flask import abort, request, jsonify


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
def get_all_amenities():
    """get all instances"""
    amenity_list = []
    amenity = storage.all(Amenity).values()
    for i in amenity:
        amenity_list.append(i.to_dict())
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False, methods=["GET"])
def get_amenities(amenity_id):
    """get amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False, methods=["DELETE"] )
def del_amenity(amenity_id):
    """DELETE """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def create_amenity():
    """creates """
    json_data = request.get_json()
    if json_data:
        new = Amenity(**json_data)
        new.save()
        return jsonify(new.to_dict()), 201
    else:
        abort(400, "Not a JSON")
    if "name" not in json_data:
        abort(400, "Missing name")


@app_views.route("/amenities/<amenity_id>", strict_slashes=False, methods=["PUT"])
def update_amenity(amenity_id):
    """updates instance"""
    json_data = request.get_json()
    if not json_data:
        abort(400, "Not a JSON")
    prev = storage.get(Amenity, amenity_id)
    if prev:
        prev.name = json_data.get("name", prev.name)
        prev.save()
        return jsonify(prev.to_dict()), 200
    else:
        abort (404)
