from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
import jwt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist




class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):

        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailed('Authentication credentials were not provided.')
        token = token[7:]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,settings.JWT_ALGORITHM)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated.')
        try:
            user = get_user_model().objects.get(id = payload['id'])
        except ObjectDoesNotExist:
            raise AuthenticationFailed('Unauthenticated.')

        if not user.is_active:
            raise AuthenticationFailed('User is not active')
        
        return user, None
