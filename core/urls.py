from django.urls import path
from .views import trigger_task, IndexView

urlpatterns = [
    path('trigger/', trigger_task, name='trigger_task'),
    path('', IndexView.as_view(), name='index'),
]