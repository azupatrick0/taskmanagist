from app import db, ma
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(db.Model):
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class UserSchema(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
user = User