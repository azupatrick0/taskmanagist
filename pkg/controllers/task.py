from flask import Flask, request, make_response, jsonify
from app import db
import re
from pkg.models.task_models import task_model, task_schema, tasks_schema

class Task:
    def init(self):
        pass

    def create(self):
        title = request.json['title']
        description = request.json['description']
        is_completed = False
        email = request.json['user_email']

        if(len(title) < 1):
            return make_response({
                'status': 400,
                'data': {
                    'message': "Title is requred",
                }
            }, 400)
        else:
            new_task = task_model(title, description, is_completed, email)

            db.session.add(new_task)
            db.session.commit()

            created_task = {
                'id': new_task.id,
                'title': new_task.title,
                'description': new_task.description,
                'is_completed': new_task.is_completed,
                'user_email': new_task.email,
            }

            return make_response({
                'status': 201,
                'data': {
                    'task': created_task
                }
            }, 201)

    def retrieve_all(self):
        email = request.json['email']

        if(not re.search(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)):
          return make_response({
                'status': 400,
                'data': {
                    'message': 'Invalid email',
                }
            }, 400)
        else:
          response = task_model.query.filter_by(email=email).all()

          if(not response):
              return make_response({
                  'status': 404,
                  'data': {
                      'message': 'Tasks not found',
                  }
              }, 404)
          else:
            return make_response({
                'status': 200,
                'data': {
                    'tasks': tasks_schema.dump(response)
                }
            }, 200)

    def retrieve_one(self, task_id):
        response = task_model.query.filter_by(id=task_id).first()

        if(not response):
            return make_response({
                'status': 404,
                'data': {
                    'message': 'Task not found',
                }
            }, 404)
        else:
          returned_task = {
              'id': response.id,
              'title': response.title,
              'description': response.description,
              'is_completed': response.is_completed,
              'user_email': response.email,
          }
          return make_response({
              'status': 200,
              'data': {
                  'task': returned_task
              }
          }, 200)

    def update(self, task_id):
        is_completed = request.json['is_completed']

        response = task_model.query.filter_by(id=task_id).first()

        if(not response):
            return make_response({
                'status': 404,
                'data': {
                    'message': 'Task not found',
                }
            }, 404)
        else:
          response.is_completed = is_completed
          
          db.session.commit()

          updated_task = {
              'id': response.id,
              'title': response.title,
              'description': response.description,
              'is_completed': is_completed,
              'user_email': response.email,
          }

          return make_response({
              'status': 200,
              'data': {
                  'task': updated_task
              }
          }, 200)

    def delete(self, task_id):
        response = task_model.query.get(task_id)

        if(not response):
            return make_response({
                'status': 404,
                'data': {
                    'message': 'Task not found'
                }
            }, 404)
        else:
          try:
            db.session.delete(response)
            db.session.commit()
            return make_response({
                'status': 200,
                'data': {
                    'message': 'task deleted successfully'
                }
            }, 200)
          except:
            return make_response({
                'status': 500,
                'data': {
                    'error': 'task deletion failed'
                }
            }, 500)

task = Task()
