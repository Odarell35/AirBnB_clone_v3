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

@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def place_reviews(place_id):
    """Handle reviews related routes for a place"""

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        reviews_list = [review.to_dict() for review in place.reviews]
        return jsonify(reviews_list)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        user_id = data.get('user_id')
        text = data.get('text')

        if not user_id:
            abort(400, 'Missing user_id')

        user = storage.get(User, user_id)
        if not user:
            abort(404)

        if not text:
            abort(400, 'Missing text')

        new_review = Review(text=text, user_id=user_id, place_id=place_id)
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def review(review_id):
    """Handle individual review routes"""

    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        review = storage.get(Review, review_id)
        if review:
            review.text = data.get("text", review.text)
            review.save()
            return jsonify(review.to_dict()), 200
        else:
            abort(404)      
