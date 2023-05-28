#!/usr/bin/python3
"""
Places handler
"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def getPlace(place_id):
    """ Gets Place """
    place = storage.get('Place', place_id)

    if not place:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, "Not a JSON")
        for key, value in request.get_json().items():
            if key not in ["user_id", "city_id",
                    "id", "created_at", "updated_at"]:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places(city_id):
    """gets places"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify([place.to_dict() for place in city.places])

    if request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'user_id' not in request.get_json():
            abort(400, 'Missing user_id')
        if not storage.get('User', request.get_json()['user_id']):
            abort(404)
        if 'name' not in request.get_json():
            abort(400, 'Missing name')
        new_p = Place(**request.get_json())
        new_p.city_id = city_id
        new_p.save()
        return jsonify(new_p.to_dict()), 201

@app_views.route('/places_search', methods=['POST'])
def places_search():
    headers = request.headers.get('Content-Type')
    if headers != 'application/json':
        abort(400, 'Not a JSON')

    if not request.get_json():
        return jsonify([places.to_dict() for
            places in storage.all('Place').values()])

    res = []
    places = []
    amenities = []
    obj = request.get_json()

    #get all cities from states if state passed
    for key, value in obj.items():
        if key == 'states':
            for item in value:
                state_obj = storage.get('State', item)
                for city in state_obj.cities:
                    res.append(city.id)

    #add cities to existing cities list after looking states
    for key, value in obj.items():
        if key == 'cities':
            for item in value:
                if item not in res:
                    res.append(item)

    #create amenities list of amenities passed
    for key, value in obj.items():
        if key == 'amenities':
            for item in value:
                if item not in res:
                    amenities.append(item)

    #create list of place id's from all cities
    for place in storage.all('Place').values():
        if place.city_id in res:
            places.append(place.id)

    #if places is empty and amenities is not empty
    if places == [] and amenities != []:
        remove = []
        res = []
        places = [place.id for place in storage.all('Place').values()]
        for place in places:
            obj = storage.get('Place', place)
            for a in obj.amenities:
                if a.id not in amenities:
                    if place not in remove:
                        remove.append(place)
        for place in places:
            if place not in remove:
                res.append(place)
        return jsonify([storage.get('Place', obj).to_dict()
            for obj in res])

    if amenities != []:
        for place in places:
            obj = storage.get('Place', place)
            for amenity in amenities:
                if amenity not in obj.amenities:
                    places.remove(place)
    return jsonify([storage.get('Place', id).to_dict() for id in places])
