from django.db import models
from account.models import User

class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    NOTIF_MESSAGE = [
        ('like', 'liked your Tweet'),
        ('comment', 'commented on your Tweet'),
        ('follow', 'started following you'),
        ('retweet', 'retweeted your Tweet'),
        ('newpost', 'posted a new Tweet'),
        ('mention', 'mentioned you in a Tweet'),
    ]
    
    type = models.CharField(max_length=50, choices=NOTIF_MESSAGE, null=True)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    tweet_id = models.ForeignKey('core.Tweet', on_delete=models.CASCADE, related_name='source_tweet', blank=True, null=True)  # Optional link for the notification

    def save(self, *args, **kwargs):
        if self.sender == self.user:
            return  # No self-notifications
        self.message = self.get_type_display()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-timestamp']  # Show newest notifications first

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"