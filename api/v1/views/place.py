#!/usr/bin/python3
"""View for State"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from flask import jsonify, abort, request, make_response
from sqlalchemy import IntegrityError


@app_views.route('/cities/<city_id>/places' methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """ lista all places in the city"""

    city_dict = storage.all(City)
    return_list = []

    place_list = storage.get(City, city_id)
    if place_list is None:
        abort(404)

    for place in place_list.places:
        return_list.append(place.to_dict())
    return jsonify(return_list)

@app_views.route('/places/<place_id>' methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    place = storage.all(Place, place_id)
    if place is not None:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>' methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete a place"""
    place = storage.all(Place, place_id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/cities/<city_id>/places' methods=['POST'])
def Create_Place(city_id):
    """ create a new place"""
    try:
        req_dict = request.get_json(silent=True)
        if req_dict is not None:
            if 'name' in req_dict.keys() and req_dict['name'] is not None:
                req_dict['city_id'] = city_id
                new = Place(**req_dict)
                new.save()
                return make_response(jsonify(new.to_dict()), 201)
            return make_response(jsonify({'error': 'Missing name'}), 400)
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    except IntegrityError:
        abort(404)

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Update a place information. """
    req_dict = request.get_json(silent=True)
    if req_dict is not None:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        for key, value in req_dict.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(place, key, value)
            storage.save()
            return make_response(jsonify(place.to_dict()), 200)
        return make_response(jsonify({'error': 'Not a JSON'}), 400)