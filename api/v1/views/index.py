#!/usr/bin/python3
"""Module"""
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """returns OK status"""
    return {

            "status": "OK"
    }


@app_views.route('/api/v1/stats', methods=['GET'])
def stats():
    """Retrieves the number of each object by type"""
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]
    stats_dict = {}

    for cls_name in classes:
        cls = storage.classes.get(cls_name)
        if cls:
            count = storage.count(cls)
            stats_dict[cls_name.lower()] = count

    return jsonify(stats_dict)
