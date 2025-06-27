#!/usr/bin/python3
"""
creates an endpoint that checks api status.
Return: json
"""
from api.v1.views import app_views
from flask import jsonify
import json
from models import storage
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.state import State
from models.user import User
from models.city import City


@app_views.route('/status', strict_slashes=False)
def view_status():
    dic = {'status': 'OK'}
    return jsonify(dic)


@app_views.route('/stats', strict_slashes=False)
def view_stats():
    dic = {'amenities': storage.count(Amenity),
           'cities': storage.count(City),
           'places': storage.count(Place),
           'reviews': storage.count(Review),
           'states': storage.count(State),
           'users': storage.count(User),
           }
    return jsonify(dic)
