#!/usr/bin/python3
"""
creates an endpoint that retrieves states objects.
Return: json
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
import json
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def view_places(city_id):
    city = storage.get(City, city_id)
    if city:
        lst = []
        for place in city.places:
            lst.append(place.to_dict())
        return jsonify(lst)
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False)
def view_a_place(place_id):
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    obj = storage.get(Place, place_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    try:
        data = request.get_json()
    except:
        return make_response(jsonify("Not a JSON"), 400)

    if not isinstance(data, dict):
        return make_response(jsonify("Not a JSON"), 400)

    if not storage.get(City, city_id):
        abort(404)

    if 'name' not in data:
        return make_response(jsonify("Missing name"), 400)

    if 'user_id' not in data:
        return make_response(jsonify("Missing user_id"), 400)

    if not storage.get(User, data['user_id']):
        abort(404)

    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)

    try:
        data = request.get_json()
    except:
        return make_response(jsonify("Not a JSON"), 400)

    if not isinstance(data, dict):
        return make_response(jsonify("Not a JSON"), 400)

    for k, v in data.items():
        if (k != 'id' and k != 'city_id' and k != 'user_id' and
           k != 'created_at' and k != 'updated_at'):
            setattr(obj, k, v)
            storage.save()

    return make_response(jsonify(obj.to_dict()), 200)


@app_views.route('/places_search',
                 strict_slashes=False, methods=['POST'])
def filter_places():
    try:
        data = request.get_json()
    except:
        return make_response(jsonify("Not a JSON"), 400)

    if not isinstance(data, dict):
        return make_response(jsonify("Not a JSON"), 400)

    place_lst = []
    if data.get('states'):
        for state_id in data['states']:
            state = storage.get(State, state_id)
            for city in state.cities:
                place_lst.extend(city.places)

    if data.get('cities'):
        for city_id in data['cities']:
            city = storage.get(City, city_id)
            for place in city.places:
                if place not in place_lst:
                    place_lst.append(place)

    if not place_lst:
        place_lst.extend(storage.all(Place).values())

    if data.get('amenities'):
        amenity_lst = []
        tmp_lst = place_lst[:]
        for amenity_id in data['amenities']:
            amenity_lst.append(storage.get(Amenity, amenity_id))
        for place in tmp_lst:
            for amenity in amenity_lst:
                if amenity not in place.amenities:
                    place_lst.remove(place)
                    break

    res = [place.to_dict() for place in place_lst]
    for dic in res:
        if dic.get('amenities'):
            del dic['amenities']
    return jsonify(res)
