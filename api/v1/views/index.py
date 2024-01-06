#!/usr/bin/python3
"""Module"""
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """returns OK status"""
    return {

            "status": "OK"
    }
