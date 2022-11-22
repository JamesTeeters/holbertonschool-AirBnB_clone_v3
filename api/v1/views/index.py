#!/usr/bin/python3
"""Documentation"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """check status"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    """counts all objects of given name"""
    count_directory = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    return jsonify(count_directory)
