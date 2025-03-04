from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    RefreshTokenView,
    IndexView,
    LoginTemplateView,
    ProfileView,
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login_user/', LoginTemplateView.as_view(), name='login_user'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("api/token/refresh/", RefreshTokenView.as_view(), name="token_refresh"),
]