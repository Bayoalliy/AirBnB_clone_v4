#!/usr/bin/python3
"""
creates an endpoint to perform CRUD operations on Amenity objects.
Return: json
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
import json
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def view_amenities(amenity_id=None):
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            return jsonify(amenity.to_dict())
        abort(404)
    lst = []
    for amenity in storage.all(Amenity).values():
        lst.append(amenity.to_dict())

    return jsonify(lst)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    obj = storage.get(Amenity, amenity_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    try:
        data = request.get_json()
    except:
        return make_response(jsonify("Not a JSON"), 400)
    if 'name' not in data:
        return make_response(jsonify("Missing name"), 400)

    new_amenity = Amenity(**data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)

    try:
        data = request.get_json()
    except:
        return make_response(jsonify("Not a JSON"), 400)

    for k, v in data.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(obj, k, v)
            storage.save()

    return make_response(jsonify(obj.to_dict()), 200)
