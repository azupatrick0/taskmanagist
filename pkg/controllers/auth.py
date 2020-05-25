from flask import Flask, request, make_response
import re
from app import db, bcrypt
from pkg.models.auth_models import user
from pkg.helpers.authentication import generateToken

class Auth:
    def init(self):
        pass

    def signup(self):
        name = request.json['name']
        email = request.json['email']
        unhashed_password = request.json['password']

        password = bcrypt.generate_password_hash(
            unhashed_password).decode('utf-8')

        if(len(email) < 1):
            return make_response({
                'status': 400,
                'data': {
                    'message': "Email is requred",
                }
            }, 400)
        elif(len(password) < 6):
            return make_response({
                'status': 400,
                'data': {
                    'message': "Password must be 6 or more characters",
                }
            }, 400)
        elif(re.search("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)):
            response = user.query.filter_by(email=email).first()

            if(response):
                return make_response({
                    'status': 409,
                    'data': {
                        'error': 'User already exists'
                    }
                }, 409)
            else:
                new_user = user(name, email, password)

                db.session.add(new_user)
                db.session.commit()

                auth_user = {
                    'id': new_user.id,
                    'name': new_user.name,
                    'email': new_user.email,
                }

                return make_response({
                    'status': 201,
                    'data': {
                        'user': {
                            **auth_user,
                            'token': generateToken(auth_user)
                        }
                    }
                }, 201)
        else:
            # email is not valid
            return make_response({
                'status': 400,
                'data': {
                    'message': "Email is invalid",
                }
            }, 400)

    def login(self):
        email = request.json['email']
        unhashed_password = request.json['password']

        response = user.query.filter_by(email=email).first()
        password = response.password

        if(not response):
            make_response({
                'status': 404,
                'data': {
                    'message': 'User not found',
                }
            }, 404)

        elif(not bcrypt.check_password_hash(password, unhashed_password)):
            make_response({
                'status': 400,
                'data': {
                    'message': 'Invalid login credentials',
                }
            }, 400)
        else:
            auth_user = {
                'id': response.id,
                'name': response.name,
                'email': response.email,
            }

            return make_response({
                'status': 200,
                'data': {
                    'user': {
                        **auth_user,
                        'token': generateToken(auth_user)
                    }
                }
            }, 200)

auth = Auth()
