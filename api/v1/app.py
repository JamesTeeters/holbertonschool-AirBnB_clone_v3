#!/usr/bin/python3
""" Documentation """
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """ closes current sesssion """
    storage.close()


@app.errorhandler(404)
def error_not_found(exception):
    """ 404 page not found error handler """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    host = '0.0.0.0'
    port = '5000'
    if getenv('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    if getenv('HBNB_API_PORT'):
        port = getenv('HBNB_API_PORT')

    app.run(host=host, port=port, threaded=True)
