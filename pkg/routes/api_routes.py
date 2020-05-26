from flask import Blueprint
from flask_jwt_extended import jwt_required
from pkg.controllers.auth import auth
from pkg.controllers.home import home

router = Blueprint('router', __name__)

@router.route('/api/v1/auth/login', methods=['POST'])
def login():
    return auth.login()

@router.route('/api/v1/auth/signup', methods=['POST'])
def signup():
    return auth.signup()

@router.route('/api/v1/', methods=['GET'])
def index():
    return home.index()
