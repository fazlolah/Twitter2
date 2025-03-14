from django.urls import path
from . import views


urlpatterns = [
    # Home Feed
    path('', views.home_feed, name='home'),

    # Tweet-related URLs
    path('post/', views.post_tweet, name='create_tweet'),
    path('tweet/<int:tweet_id>/delete/', views.delete_tweet, name='delete_tweet'),
    path('tweet/<int:tweet_id>/edit/', views.edit_tweet, name='edit_tweet'),


    # Like/Unlike URLs
    path('tweet/<int:tweet_id>/like/', views.like_tweet, name='like_tweet'),

    # Retweet URLs
    path('tweet/<int:tweet_id>/retweet/', views.retweet_tweet, name='retweet_tweet'),

    # Reply
    path('tweet/<int:tweet_id>/reply/', views.post_reply, name='post_reply'),

    # Follow/Unfollow URLs
    path('user/<int:user_id>/follow/', views.follow_user, name='follow_user'),
    path('user/<int:user_id>/unfollow/', views.unfollow_user, name='unfollow_user'),

    # Search URL
    path('explore/', views.explore_feed, name='explore'),
    path('explore/<slug:tag>', views.explore_tag, name='explore_tag'),
    path('explore/search/', views.search, name='search'),

    path('tweet/<int:tweet_id>/', views.view_tweet, name='view_tweet'),
    path('user/<str:username>/<int:tweet_id>/', views.view_tweet, name='view_tweet'),


]