#!/usr/bin/python3
"""
creates an endpoint that retrieves states objects.
Return: json
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
import json
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
@app_views.route('/states/<state_id>', strict_slashes=False)
def view_states(state_id=None):
    if state_id:
        res = storage.get(State, state_id)
        if res:
            return jsonify(res.to_dict())
        abort(404)
    lst = []
    for state in storage.all(State).values():
        lst.append(state.to_dict())

    return jsonify(lst)


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    obj = storage.get(State, state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    try:
        data = request.get_json()
    except:
        return make_response(jsonify("Not a JSON"), 400)
    if 'name' not in data:
        return make_response(jsonify("Missing name"), 400)

    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    obj = storage.get(State, state_id)
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
