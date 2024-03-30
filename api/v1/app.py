#!/usr/bin/python3
"""
The Script creates contains the flask blueprint
"""
import os

from flask import Flask, jsonify, request
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)

app.url_map.strict_slashes = False

print(app.url_map)


@app.teardown_appcontext
def close_connection(exception):
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = os.environ.get("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True, debug=True)
