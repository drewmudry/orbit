# django-oauth/core/users/auth.py

import jwt
from datetime import datetime, timedelta
from django.conf import settings

def create_session_cookie(user):
    """Create a session cookie for cross-app authentication."""
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': int((datetime.utcnow() + timedelta(days=7)).timestamp()),  # Convert to timestamp
        'iat': int(datetime.utcnow().timestamp())  # Convert to timestamp
    }
    
    # Use settings.SECRET_KEY if JWT_SECRET_KEY is not defined
    secret_key = getattr(settings, 'JWT_SECRET_KEY', settings.JWT_SECRET_KEY)
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    print(f"Generated token: {token}")
    
    return token

def validate_session_cookie(token):
    """Validate a session cookie and return the user."""
    try:
        # Use settings.SECRET_KEY if JWT_SECRET_KEY is not defined
        secret_key = getattr(settings, 'JWT_SECRET_KEY', settings.JWT_SECRET_KEY)
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        from .models import User
        user = User.objects.get(id=payload['user_id'])
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
        return None