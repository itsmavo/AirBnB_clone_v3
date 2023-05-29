#!/usr/bin/python3
"""
places amenities
"""
from flask import Flask, make_response, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def place_allAmenities(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not place.amenities:
        return jsonify([])
    return jsonify([a.to_dict() for a in place.amenities])

@app_views.route('/places/<place_id>/amenities/<amenity_id>',
        methods=['DELETE', 'POST'], strict_slashes=False)
def place_amenity(place_id, amenity_id):
    a = storage.get(Amenity, amenity_id)
    p = storage.get(Place, place_id)
    if not a or not p:
        abort(404)

    if request.method == 'DELETE':
        if a not in place.amenities:
            abort(404)
        storage.delete(a)
        storage.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if a not in place.amenities:
            place.amenities.append(a)
            place.save()
            return jsonify(a.to_dict()), 201
        return jsonify(a.to_dict()), 200
