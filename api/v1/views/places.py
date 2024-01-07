#!/usr/bin/python3
"""
Place objects that handles all default RESTFul API actions
"""

from flask import Flask, jsonify, request, abort
from models import Place, City, User

app = Flask(__name__)


@app.route('/api/v1/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
	"""Retrieves the list of all Place objects of a City"""
    city = City.get(city_id)
    if not city:
        abort(404)
    places = Place.get_places_by_city(city_id)
    return jsonify([place.to_dict() for place in places])


@app.route('/api/v1/places/<place_id>', methods=['GET'])
def get_place(place_id):
	"""Retrieves a Place object"""
    place = Place.get(place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app.route('/api/v1/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
	"""Deletes a Place object"""
    place = Place.get(place_id)
    if not place:
        abort(404)
    place.delete()
    return jsonify({}), 200


@app.route('/api/v1/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
	"""Creates a Place"""
    city = City.get(city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    user_id = data.get('user_id')
    if not user_id:
        abort(400, 'Missing user_id')
    user = User.get(user_id)
    if not user:
        abort(404)

    name = data.get('name')
    if not name:
        abort(400, 'Missing name')

    place = Place(city_id=city_id, user_id=user_id, name=name)
    place.save()
    
    return jsonify(place.to_dict()), 201


@app.route('/api/v1/places/<place_id>', methods=['PUT'])
def update_place(place_id):
	"""Updates a Place object"""
    place = Place.get(place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200
