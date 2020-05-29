from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from pkg.controllers.auth import auth
from pkg.controllers.home import home
from pkg.controllers.task import task

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

@router.route('/api/v1/task/create', methods=['POST'])
@jwt_required
def create():
    return task.create()

@router.route('/api/v1/task/retrieve', methods=['GET'])
@jwt_required
def retrieve_all():
    return task.retrieve_all()

@router.route('/api/v1/task/retrieve/<task_id>', methods=['GET'])
@jwt_required
def retrieve_one(task_id):
    return task.retrieve_one(task_id)

@router.route('/api/v1/task/update/<task_id>', methods=['PUT'])
@jwt_required
def update(task_id):
    return task.update(task_id)

@router.route('/api/v1/task/delete/<task_id>', methods=['DELETE'])
@jwt_required
def delete(task_id):
    return task.delete(task_id)