#!/usr/bin/python3
"""
Review object that handles all default RESTFul API actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def place_reviews(place_id):
    """Handle reviews related routes for a place"""
    list_review= []
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    review_obj = place.reviews
    for r in review_obj:
        list_review.append(r.to_dict())
    return jsonify(list_review)


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["GET"])
def fetch_review(review_id):
    """gets review"""
    obj = storage.get(Review, review_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["DELETE"])
def delete_review(review_id):
    """deletes review"""
    obj = storage.get(Review, review_id)
    if obj:
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def creates_r(place_id):
    """creates review instance"""
    json_data = request.get_json()
    if not json_data:
        abort(400, "Not a JSON")
    if "user_id" not in json_data:
        abort(400, "Missing user_id")
    if "text" not in json_data:
        abort(400, "Missing text")
    user = storage.get(User, json_data["user_id"])
    if user is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place:
        json_data['place_id'] = place_id
        new_review = Review(**json_data)
        new_review.save()
        return jsonify(new_review.to_dict()), 201
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["PUT"])
def update_r(review_id):
    """updates review"""
    json_data = request.get_json()
    if not json_data:
        abort(400, "Not a JSON")
    old_r =storage.get(Review, reivew_id)
    if old_r:
        old_r.test = json_data.get('test', old_r.text)
        old_r.save()
        return jsonify(old_r.to_dict()), 200
    else:
        abort (404)
