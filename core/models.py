from django.db import models
from account.models import User
from django.utils.text import slugify
from .utils import extract_hashtags, extract_mentions
from notification.models import Notification
# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"#{self.name}"

class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=450, null=False, blank=False)
    image = models.ImageField(upload_to='tweets/', blank=True, null=True)
    
    tags = models.ManyToManyField(Tag, related_name='tweets', blank=True)  # Add this line

    sentiment = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at', 'author']),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the tweet first

        hashtags = extract_hashtags(self.text)
        for hashtag in hashtags:
            tag, created = Tag.objects.get_or_create(name=hashtag.lower())
            self.tags.add(tag)

        mentions = extract_mentions(self.text)
        for mention in mentions:
            Notification.objects.create(
                sender_id=self.author.id,
                user=User.objects.get(username=mention.lstrip('@')),
                type="mention",
                tweet_id=self  # Link to the tweet
            )

    def __str__(self):
        return f"{self.author.username}: {self.text[:50]}..."

    def how_long_ago(self):
        from django.utils.timesince import timesince
        return timesince(self.created_at)

    def like_count(self):
        return self.likes.count()
    
    def retweet_count(self):
        return self.retweets.count()

    def user_has_liked(self, user):
        return self.likes.filter(user=user).exists()

class Comment(Tweet):
    post = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')  # The post the comment belongs to
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')  # A self-referential field for nested comments
    
    def __str__(self):
        return f"{self.author.username}: {self.text[:25]}..."  # Show first 20 characters of the comment

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:

        constraints = [
            models.UniqueConstraint(fields=['follower', 'followed'], name='unique_follow')
        ]

        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:

        constraints = [
            models.UniqueConstraint(fields=['user', 'tweet'], name='unique_like')
        ]

        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} likes tweet {self.tweet.id}"

class Retweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=450, null=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='retweets')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'tweet'], name='unique_retweet')
        ]

    def __str__(self):
        return f"{self.user.username} retweeted tweet {self.tweet.id}"
    