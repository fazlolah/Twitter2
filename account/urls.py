from django.urls import path
from account import views

urlpatterns = [
    # path('', views.user_account, name='profile'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('forgot-password/', views.forgotpassword_page, name='forgot-password'),
    path('logout/', views.user_logout, name='logout'),

    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('<str:username>/', views.user_profile, name='user_profile'),
    path('<str:username>/follows', views.follows_list_view, name='follows_list'),

]
