#!/usr/bin/python3
""" view for City objects """
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from flask import jsonify, abort, request, make_response
from sqlalchemy.exc import IntegrityError


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def place_list(city_id):
    """ lists all palce objects """
    cities_dict = storage.all(City)
    return_list = []

    cities_list = storage.get(City, city_id)
    if cities_list is None:
        abort(404)
    for place in cities_list.places:
        return_list.append(place.to_dict())
    return jsonify(return_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def grab_place(place_id):
    """ Grabs a palce object """
    place = storage.get(Place, place_id)
    if place is not None:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Delete a place """
    place = storage.get(Place, place_id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def new_place(city_id):
    """ Create a new place """
    try:
        r_dict = request.get_json(silent=True)
        if r_dict is not None:
            if 'name' in r_dict.keys() and r_dict['name'] is not None:
                if 'user_id'in r_dict.keys() and r_dict['user_id'] is not None:
                    r_dict['city_id'] = city_id
                    new_place = Place(**r_dict)
                    new_place.save()
                    return make_response(jsonify(new_place.to_dict()), 201)
                return make_response(jsonify({'error': 'Missing user_id'}),
                                     400)
            return make_response(jsonify({'error': 'Missing name'}), 400)
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    except IntegrityError:
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Update a place obj """
    req_dict = request.get_json(silent=True)
    if req_dict is not None:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        for key, value in req_dict.items():
            if key not in ['id', 'user_id', 'city_id',
                           'created_at', 'updated_at']:
                setattr(place, key, value)
            storage.save()
            return make_response(jsonify(place.to_dict()), 200)
    return make_response(jsonify({'error': 'Not a JSON'}), 400)
