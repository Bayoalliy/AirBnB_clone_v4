#!/usr/bin/python3
"""
creates an endpoint to perform CRUD operations on User objects.
Return: json
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
import json
from models import storage
from models.user import User
from hashlib import md5


@app_views.route('/users', strict_slashes=False)
@app_views.route('/users/<user_id>', strict_slashes=False)
def view_users(user_id=None):
    if user_id:
        user = storage.get(User, user_id)
        if user:
            return jsonify(user.to_dict())
        abort(404)
    lst = []
    for user in storage.all(User).values():
        lst.append(user.to_dict())

    return jsonify(lst)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    obj = storage.get(User, user_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    try:
        data = request.get_json()
    except:
        return make_response(jsonify("Not a JSON"), 400)

    if not isinstance(data, dict):
        return make_response(jsonify("Not a JSON"), 400)

    if 'email' not in data:
        return make_response(jsonify("Missing email"), 400)
    if 'password' not in data:
        return make_response(jsonify("Missing password"), 400)

    new_user = User(**data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)

    try:
        data = request.get_json()
    except:
        return make_response(jsonify("Not a JSON"), 400)

    if not isinstance(data, dict):
        return make_response(jsonify("Not a JSON"), 400)

    if "password" in data:
        pwd = data['password']
        data['password'] = md5(pwd.encode()).hexdigest()

    for k, v in data.items():
        if (k != 'id' and k != 'created_at' and
           k != 'updated_at'and k != 'email'):
            setattr(obj, k, v)
    storage.save()

    return make_response(jsonify(obj.to_dict()), 200)
