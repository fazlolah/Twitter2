from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_direct_messages, name='messages'),
    path('send_message/', views.send_direct_message, name='send_direct_message'),
    path('send_message/<int:receiver_id>/', views.send_direct_message, name='send_direct_message_to_user'),
    path('direct/<int:user_id>/', views.view_conversation, name='view_conversation'),
]