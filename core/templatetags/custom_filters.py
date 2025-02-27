from django import template
from core.models import Like

register = template.Library()

@register.filter
def user_has_liked(tweet, user):
    return tweet.likes.filter(user=user).exists()

@register.filter
def user_has_retweeted(tweet, user):
    return tweet.retweets.filter(user=user).exists()