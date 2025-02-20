from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_notifications, name='notifications'),
    path('mark_as_read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('mark_all_as_read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
]