from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta, timezone

def generateToken(user):
  identity = {
      'iss': 'https://taskmanagist.netlify.app',
      'sub': user,
      'iat': datetime.now(timezone.utc),
      'exp': datetime.now(timezone.utc) + timedelta(hours=24),
  }

  token = create_access_token(identity = identity)

  return token

generateToken = generateToken