#!/usr/bin/python3
"""
creates an endpoint to perform crud operations on review objects.
Return: json
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
import json
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def view_reviews(place_id):
    place = storage.get(Place, place_id)
    if place:
        lst = []
        for review in place.reviews:
            lst.append(review.to_dict())
        return jsonify(lst)
    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def view_a_review(review_id):
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    obj = storage.get(Review, review_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def create_review(place_id):
    try:
        data = request.get_json()
    except:
        return make_response(jsonify("Not a JSON"), 400)

    if not isinstance(data, dict):
        return make_response(jsonify("Not a JSON"), 400)

    if not storage.get(Place, place_id):
        abort(404)

    if 'text' not in data:
        return make_response(jsonify("Missing text"), 400)

    if 'user_id' not in data:
        return make_response(jsonify("Missing user_id"), 400)

    if not storage.get(User, data['user_id']):
        abort(404)

    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)

    try:
        data = request.get_json()
    except:
        return make_response(jsonify("Not a JSON"), 400)

    if not isinstance(data, dict):
        return make_response(jsonify("Not a JSON"), 400)

    for k, v in data.items():
        if (k != 'id' and k != 'place_id' and k != 'user_id' and
           k != 'created_at' and k != 'updated_at'):
            setattr(obj, k, v)
            storage.save()

    return make_response(jsonify(obj.to_dict()), 200)
