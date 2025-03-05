from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser

class JWTCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Verifica se há um token JWT no cookie
        access_token = request.COOKIES.get("access_token")
        if access_token:
            try:
                validated_token = JWTAuthentication().get_validated_token(access_token)
                user = JWTAuthentication().get_user(validated_token)
                request.user = user  # Define o usuário autenticado na request
            except Exception:
                request.user = AnonymousUser()  # Se o token for inválido, trata como anônimo
        else:
            request.user = AnonymousUser()  # Se não houver token, trata como anônimo
