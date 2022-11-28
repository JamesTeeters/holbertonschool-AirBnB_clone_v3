#!/usr/bin/python3
""" view for City objects """
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request, make_response
from sqlalchemy.exc import IntegrityError


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def city_list(state_id):
    """ lists all City objects """
    states_dict = storage.all(State)
    cities_list = None
    return_list = []

    for state in states_dict.values():
        if state.id == state_id:
            cities_list = state.cities
        if cities_list is None:
            abort(404)
        for city in cities_list:
            return_list.append(city.to_dict())
        return jsonify(return_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def grab_city(city_id):
    """ Grabs a city object """
    city = storage.get(City, city_id)
    if city is not None:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Delete a city """
    city = storage.get(City, city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states/<state_id>', methods=['POST'], strict_slashes=False)
def new_city(state_id):
    """ Create a new city """
    try:
        req_dict = request.get_json(silent=True)
        if req_dict is not None:
            if 'name' in req_dict.keys() and req_dict['name'] is not None:
                req_dict['state_id'] = state_id
                new = City(**req_dict)
                new.save()
                return make_response(jsonify(new.to_dict()), 201)
            return make_response(jsonify({'error': 'Missing name'}), 400)
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    except IntegrityError:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Update a city obj """
    req_dict = request.get_json(silent=True)
    if req_dict is not None:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        for k, v in req_dict.items():
            if k not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, k, v)
            storage.save()
            return make_response(jsonify(city.to_dict()), 200)
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
