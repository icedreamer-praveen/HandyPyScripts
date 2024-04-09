
import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse


def decode_jwt_token(token):
    """
    This function decodes a JWT token to extract the user information.

    Parameters:
    - token (str): The JWT token to decode.

    Returns:
    - User: The user object associated with the provided token if it is valid and not expired.
    - None: If the token is invalid or expired, or if an error occurs during decoding.

    Exceptions:
    - jwt.ExpiredSignatureError: Raised if the token has expired.
    - jwt.InvalidTokenError: Raised if the token is invalid.
    """
    try:
        token = token.split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']

        user = User.objects.get(id=user_id)
        return user
    
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    

def some_view(request):
    """
    This function is a view for handling user authentication based on a JWT token.

    Parameters:
    - request (HttpRequest): An HTTP request object containing headers.

    Returns:
    - JsonResponse: A JSON response indicating the authentication status.
    - If a valid token is provided and successfully decoded, the function returns a success message.
    - If no token is provided or the token is invalid or expired, the function returns an error message with the HTTP status code 401 Unauthorized.
    """
    token = request.headers.get('Authorization')

    if token:
        user = decode_jwt_token(token)

        if user:
            return JsonResponse({'message': 'User authenticated successfully'})
        else:
            return JsonResponse({'message': 'Invalid or expired token'}, status=401)
    else:
        return JsonResponse({'message': 'No token provided'}, status=401)