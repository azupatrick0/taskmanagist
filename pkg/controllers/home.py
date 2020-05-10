from flask import jsonify

class Home:
    def init(self):
        pass

    def index(self):
        return jsonify({
            'data': {
                'message': 'Welcome to taskmanagist api, the best api in the world that helps you manage your tasks easily'
            }
        })

home = Home()