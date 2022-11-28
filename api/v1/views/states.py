#!/usr/bin/python3
"""View for State"""
from flask import jsonify, abort, request, make_response
from sqlalchemy.exc import IntegrityError
from api.v1.views import app_views
from models import storage
from models.state import State




@app_views.route('/states', methods=['GET'],
                 strict_slashes=False)
def api_states():
    """return list of all states"""
    all_states = []
    states_dict = storage.all(State)
    for state in states_dict.values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def api_state(state_id):
    """return state with given id"""
    for state in storage.all(State).values():
        if state.id == state_id:
            return (state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def api_delete_state(state_id):
    for state in storage.all(State).values():
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def api_create_state():
    """create new state"""
    try:
        req_dict = request.get_json(silent=True)
        if req_dict is not None:
            if 'name' in req_dict.keys() and req_dict['name'] is not None:
                new_state = State(**req_dict)
                new_state.save()
                return make_response(jsonify(new_state.to_dict()), 201)
            return make_response(jsonify({'error': 'Missing name'}), 400)
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    except IntegrityError:
        abort(404)


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def api_update_state(state_id):
    """Update state"""
    req_dict = request.get_json(silent=True)
    if req_dict is not None:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        for key, value in req_dict.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
            storage.save()
            return make_response(state.to_dict(), 200)
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
