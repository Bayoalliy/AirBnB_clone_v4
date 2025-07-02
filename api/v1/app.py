#!/usr/bin/python3
"""
entry point
register app_views blueprint
close connection
"""
from flask import Flask, jsonify, make_response
from os import getenv
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
api_host = getenv("HBNB_API_HOST")
api_port = getenv("HBNB_API_PORT")

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_connection(exception):
    """close cureent connection"""
    storage.close()


@app.errorhandler(404)
def error_page(err):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=api_host, port=api_port, threaded=True)
