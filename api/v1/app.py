#!/usr/bin/python3
"""api doc"""

from flask import Flask
from models import storage
from api.v1.views import app_views
#from flask_cors import CORS

app = Flask(__name__)


app.register_blueprint(app_views)
#CORS(app, resources={'/*': {'origins': '0.0.0.0'}})
app.url_map.strict_slashes = False

@app.teardown_appcontext
def closing(cont):
    """ method docs"""
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    """handler"""
    return {"error": "Not found"}, 404

if __name__ == "__main__":
    import os
    if os.getenv("HBNB_API_HOST"):
        host = os.getenv("HBNB_API_HOST")
    else:
        host = '0.0.0.0'
    if os.getenv("HBNB_API_PORT"):
        port = int(os.getenv("HBNB_API_PORT"))
    else:
        port = 5000
    app.run(host=host, port=port, threaded=True)
