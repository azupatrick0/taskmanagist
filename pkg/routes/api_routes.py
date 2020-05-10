from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.auth import auth
from controllers.home import home

router = Blueprint('router', __name__)

@router.route('/api/v1/auth/login', methods=['POST'])
def login():
    print('login')
    return auth.login()

@router.route('/api/v1/auth/signup', methods=['POST'])
def signup():
    print('signing up')
    return auth.signup()

@router.route('/api/v1/', methods=['GET'])
@jwt_required
def index():
    return home.index()
