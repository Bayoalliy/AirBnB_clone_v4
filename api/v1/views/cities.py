#!/usr/bin/python3
"""
creates an endpoint to perform CRUD operarions on  City objects.
Return: json
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
import json
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def view_cities(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    lst = []
    for city in state.cities:
        lst.append(city.to_dict())

    return jsonify(lst)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def view_city_by_id(city_id):
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    obj = storage.get(City, city_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):
    try:
        data = request.get_json()
    except:
        return make_response(jsonify("Not a JSON"), 400)
    if 'name' not in data:
        return make_response(jsonify("Missing name"), 400)

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data['state_id'] = state.id
    new_city = City(**data)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    try:
        data = request.get_json()
    except:
        return make_response(jsonify("Not a JSON"), 400)

    for k, v in data.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(city, k, v)
            storage.save()

    return make_response(jsonify(city.to_dict()), 200)
