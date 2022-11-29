#!/usr/bin/python3
""" view for City objects """
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from flask import jsonify, abort, request, make_response
from sqlalchemy.exc import IntegrityError


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def review_list(place_id):
    """ lists all review objects """
    places_dict = storage.all(Place)
    return_list = []

    places_list = storage.get(Place, place_id)
    if places_list is None:
        abort(404)
    for review in places_list.reviews:
        return_list.append(review.to_dict())
    return jsonify(return_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def grab_review(review_id):
    """ Grabs a review object """
    review = storage.get(Review, review_id)
    if review is not None:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Delete a review """
    review = storage.get(Review, review_id)
    if review is not None:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def new_review(place_id):
    """ Create a new review """
    try:
        req_dict = request.get_json(silent=True)
        if req_dict is not None:
            if 'user_id' in req_dict.keys() and req_dict['user_id'] is not None:
                if 'text' in req_dict.keys() and req_dict['text'] is not None:
                    req_dict['place_id'] = place_id
                    new_review = Review(**req_dict)
                    new_review.save()
                    return make_response(jsonify(new_review.to_dict()), 201)
                return make_response(jsonify({'error': 'Missing text'}), 400)
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    except IntegrityError:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Update a review obj """
    req_dict = request.get_json(silent=True)
    if req_dict is not None:
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        for key, value in req_dict.items():
            if key not in ['id', 'user_id', 'place_id',
                           'created_at', 'updated_at']:
                setattr(review, key, value)
            storage.save()
            return make_response(jsonify(review.to_dict()), 200)
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
