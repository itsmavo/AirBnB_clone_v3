#!/usr/bin/python3
"""
amenities handler
"""
from flask import Flask, make_response, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def all_amenities():
    if request.method == 'GET':
        return jsonify([a.to_dict()
                        for a in storage.all(Amenity).values()])
    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'name' not in request.json:
            abort(400, 'Missing name')
        new_a = Amenity(**request.get_json())
        new_a.save()
        return make_response(jsonify(new_a.to_dict()), 201)

@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def amenity(amenity_id):
    a = storage.get(Amenity, amenity_id)

    if not a:
        abort(404)
        
    if request.method == 'GET':
        return make_response(jsonify(a.to_dict()), 200)

    if request.method == 'DELETE':
        storage.delete(a)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(a, key, value)
        a.save()
        return make_response(jsonify(a.to_dict()), 200)
