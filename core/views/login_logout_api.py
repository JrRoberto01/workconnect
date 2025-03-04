from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import login, logout
from django.middleware.csrf import get_token
from rest_framework.permissions import AllowAny


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            response = Response({"message": "Login realizado com sucesso!"})

            # Criar sessão Django para que o request.user seja reconhecido
            login(request, user)

            # Definir cookies para autenticação JWT
            response.set_cookie(
                key="access_token",
                value=str(refresh.access_token),
                httponly=True,
                secure=True,  # Defina como False para desenvolvimento sem HTTPS
                samesite="Lax",
            )
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="Lax",
            )

            # Adiciona CSRF Token no cookie para proteger requisições POST futuras
            response.set_cookie(
                key="csrftoken",
                value=get_token(request),
                httponly=False,
                secure=True,
                samesite="Lax",
            )

            return response
        else:
            return Response({"error": "Credenciais inválidas"}, status=401)


class LogoutView(APIView):
    permission_classes = [AllowAny]  # Permite qualquer um acessar essa view

    def post(self, request):
        logout(request)  # Finaliza a sessão Django

        response = Response({"message": "Logout realizado com sucesso!"}, status = 200)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.delete_cookie("csrftoken")
        return response

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Token não encontrado"}, status=400)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response({"message": "Token atualizado!"})
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="Lax",
            )
            return response
        except Exception as e:
            return Response({"error": "Token inválido"}, status=400)
