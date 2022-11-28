#!/usr/bin/python3
""" view for Amenity objects """
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request, make_response
from sqlalchemy.exc import IntegrityError


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenity_list():
    """ lists all amenity objects """
    amen_dict = storage.all(Amenity)
    amen_list = []
    for amenity in amen_dict.values():
        amen_list.append(amenity.to_dict())
    return jsonify(amen_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def grab_amenity(amenity_id):
    """ Grabs an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Delete an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Create an Amenity object """
    req_dict = request.get_json(silent=True)
    if req_dict is not None:
        if 'name' in req_dict.keys() and req_dict['name'] is not None:
            new_amen = Amenity(**req_dict)
            new_amen.save()
            return make_response(jsonify(new_amen.to_dict()), 201)
        return make_response(jsonify({'error': 'Missing name'}), 400)
    return make_response(jsonify({'error': 'Not a JSON'}), 400)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Update an Amenity object """
    req_dict = request.get_json(silent=True)
    if req_dict is not None:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        for k, v in req_dict.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, k, v)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    return make_response(jsonify({'error': 'Not a JSON'}), 400)
