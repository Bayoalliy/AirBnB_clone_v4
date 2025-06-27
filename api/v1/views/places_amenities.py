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
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def view_linked_amenities(place_id):
    place = storage.get(Place, place_id)
    if place:
        lst = []
        for amenity in place.amenities:
            lst.append(amenity.to_dict())
        return jsonify(lst)
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def unlink_amenity(amenity_id, place_id):
    place = storage.get(Place, place_id)
    amenity_obj = storage.get(Amenity, amenity_id)
    if place and amenity_obj:
        place.amenities.remove(amenity_obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)

    place.amenities.append(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
