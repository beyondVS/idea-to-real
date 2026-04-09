from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('session/<uuid:session_id>/', views.detail, name='detail'),
    path('create/', views.create_session, name='create_session'),
    path('session/<uuid:session_id>/send/', views.send_message, name='send_message'),
]
