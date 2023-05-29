#!/usr/bin/python3
"""
cities path handler
"""
from flask import request, jsonify, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'DELETE', 'PUT'],
		strict_slashes=False)
def city(city_id):
    city = storage.get('City', city_id)
    if not city:
        abort (404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'], strict_slashes=False)
def cities_of_State(state_id):
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        state = storage.get('State', state_id)
        return jsonify([city.to_dict() for city in state.cities])

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'name' not in request.json:
            abort(400, 'Missing name')
        new_c = City(**request.get_json())
        new_c.state_id = state.id
        new_c.save()
        return jsonify(new_c.to_dict()), 201
