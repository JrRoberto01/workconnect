from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    RefreshTokenView,
    IndexView,
    LoginTemplateView,
    ProfileView,
    ChatView,
    CreateOrgView,
    GroupView,
    GroupDetailView,

    follow_unfollow,
    load_more_messages,
)
from .views.agenda import AgendaView, deletar_evento

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login_user/', LoginTemplateView.as_view(), name='login_user'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profileid'),
    path('chat', ChatView.as_view(), name='chat'),
    path('login_user', LoginTemplateView.as_view(), name='login_user'),
    path('profile/<int:id>/', ProfileView.as_view(), name='profile'),
    path("chat/", ChatView.as_view(), name='chat'),
    path("chat/<int:user_id>/", ChatView.as_view(), name="sala_chat"),
    path('chat/load-messages/<str:room_name>/', load_more_messages, name='load_more_messages'),
    path('group', GroupView.as_view(), name='group'),
    path('group-detail/<int:id>/', GroupDetailView.as_view(), name='group-detail'),
    path('create-organization', CreateOrgView.as_view(), name='create-organization'),

    #API's
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("api/token/refresh/", RefreshTokenView.as_view(), name="token_refresh"),

    path('follow/<int:user_id>/', follow_unfollow.follow, name='follow'),
    path('unfollow/<int:user_id>/', follow_unfollow.unfollow, name='unfollow'),

    path('agenda/', AgendaView.as_view(), name='agenda_view'),
    path('agenda/deletar/<int:evento_id>/', deletar_evento, name='deletar_evento'),

]