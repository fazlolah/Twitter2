from django.contrib import admin
from core.models import Tweet, Comment, Follow, Like, Tag

# Register your models here.

admin.site.register([Tweet, Comment, Follow, Like, Tag])