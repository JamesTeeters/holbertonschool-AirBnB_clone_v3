#!/usr/bin/python3
""" view for User objects """
from api.v1.views import app_views
from models import storage
from models.users import User
from flask import jsonify, abort, request, make_response
from sqlalchemy.exc import IntegrityError


@app_views.route('/users', methods=['GET'], strictslashes=False)
def users_list():
    """ lists all User objects """
    user_dict = storage.all(User)
    user_list = []
    for user in user_dict.values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strictslashes=False)
def grab_user(user_id):
    """ Grabs a User object """
    user = storage.get(User, user_id)
    if user is not None:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strictslashes=False)
def delete_user(user_id):
    """ Delete a User object """
    user = storage.get(User, user_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/users', methods=['POST'], strictslashes=False)
def create_user():
    """ Create a User object """
    req_dict = request.get_json(silent=True)
    if req_dict is not None:
        if 'email' not in req_dict.keys() or req_dict['email'] is None:
            return make_response(jsonify({'error': 'Missing email'}), 400)
        if 'password' not in req_dict.keys() or req_dict['password'] is None:
            return make_response(jsonify({'error': 'Missing password'}), 400)
        new_user = User(**req_dict)
        new_user.save()
        return make_response(jsonify(new_user.to_dict()), 201)
    return make_response(jsonify({'error: Not a JSON'}), 400)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strictslashes=False)
def update_user(user_id):
    """ Update a User object """
    req_dict = request.get_json(silent=True)
    if req_dict is not None:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        for k, v in req_dict.items():
            if k not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, k, v)
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
    return make_response(jsonify({'error': 'Not a JSON'}), 400)
