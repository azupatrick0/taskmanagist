from app import db, ma
from pkg.models.auth_models import user

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    is_completed = db.Column(db.Boolean , nullable=False, default=False)
    email = db.Column(db.String(), db.ForeignKey('user.email'),
        nullable=False)
    user = db.relationship(user,
        backref=db.backref('tasks', lazy=True))

    def __init__(self, title, description, is_completed, email):
        self.title = title
        self.description = description
        self.is_completed = is_completed
        self.email = email

class TaskSchema(ma.Schema):

    class Meta:
        fields = ('id', 'title', 'description', 'is_completed', 'email')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
task_model = Task