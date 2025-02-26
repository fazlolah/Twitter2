from django import forms
from core.models import Tweet, User, Comment

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'image']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'w-full border-none resize-none text-xl placeholder-gray-600 focus:ring-0',
                'placeholder': "What's happening?",
                'rows': 3,
            }),
            'image': forms.FileInput(attrs={
                'hidden':True,
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'image']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'w-full border-none resize-none focus:ring-0 text-lg placeholder-gray-500',
                'placeholder': 'Tweet your reply...',
                'rows': 2,
            }),
            'image': forms.FileInput(attrs={
                'hidden':True,
            }),
        }




