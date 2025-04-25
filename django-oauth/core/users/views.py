# django-oauth/core/users/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
import json

from .auth import create_session_cookie, validate_session_cookie
from .models import User

@csrf_exempt
def api_login(request):
    """API endpoint for user login."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    if not email or not password:
        return JsonResponse({'error': 'Email and password are required'}, status=400)
    
    user = authenticate(request, email=email, password=password)
    
    if user is not None:
        login(request, user)
        
        # Create token for cross-app authentication
        token = create_session_cookie(user)
        
        # Prepare the response
        response = JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })
        
        # Set the cross-app cookie
        response.set_cookie(
            'connect_user',
            token,
            domain=settings.COOKIE_DOMAIN,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            max_age=7 * 24 * 60 * 60  # 7 days in seconds
        )
        
        return response
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

@csrf_exempt
def api_logout(request):
    """API endpoint for user logout."""
    logout(request)
    
    response = JsonResponse({'success': True})
    response.delete_cookie('connect_user', domain='.creovia.io')
    
    return response

def validate_token(request):
    """API endpoint to validate a token."""
    # Accept token either as query param or from cookie
    token = request.GET.get('token') or request.COOKIES.get('connect_user')
    
    if not token:
        return JsonResponse({'valid': False, 'error': 'No token provided'}, status=400)
    
    user = validate_session_cookie(token)
    if user:
        return JsonResponse({
            'valid': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })
    
    return JsonResponse({'valid': False, 'error': 'Invalid token'}, status=401)

def get_current_user(request):
    """API endpoint to get the current authenticated user."""
    token = request.COOKIES.get('connect_user')
    
    if not token:
        return JsonResponse({'authenticated': False}, status=401)
    
    user = validate_session_cookie(token)
    if user:
        return JsonResponse({
            'authenticated': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })
    
    return JsonResponse({'authenticated': False}, status=401)