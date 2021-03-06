from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from os import environ
from dotenv import load_dotenv

load_dotenv()

# Init App
def initialize_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')
  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400
  return app

App = initialize_app()

CORS(App)

JWTManager(App)

bcrypt = Bcrypt(App)

db = SQLAlchemy(App)

ma = Marshmallow(App)

@App.before_first_request
def create_tables():
    db.create_all()

@App.errorhandler(404)
def not_found(error):
    response = jsonify({
        'status': 404,
        'error': str(error)
    })
    response.status_code = 404
    return response

@App.errorhandler(405)
def method_not_allowed(error):
    response = jsonify({
        'status': 405,
        'error': str(error)
    })
    response.status_code = 405
    return response

@App.errorhandler(500)
def internal_server_error(error):
    response = jsonify({
        'status': 500,
        'error': str(error)
    })
    response.status_code = 500
    return response

from pkg.routes.api_routes import router
App.register_blueprint(router)