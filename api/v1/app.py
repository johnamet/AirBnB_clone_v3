#!/usr/bin/python3
"""
This script creates a Flask application with a blueprint for API endpoints.
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage

app = Flask(__name__)  # Initialize Flask app
app.register_blueprint(app_views)  # Register blueprint for API routes

# Allow routes without trailing slashes
app.url_map.strict_slashes = False

# Enable CORS for all API routes
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_connection(exception):
    """
    Close the connection to the storage.
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    """
    Custom error handler for 404 Not Found errors.
    """
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    # Get host and port from environment variables, or use default values
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = os.environ.get("HBNB_API_PORT", 5000)
    # Run the Flask application
    app.run(host=host, port=port, threaded=True)
