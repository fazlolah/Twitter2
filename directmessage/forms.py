from django import forms
from .models import DirectMessage

class DirectMessageForm(forms.ModelForm):
    class Meta:
        model = DirectMessage
        fields = ['receiver', 'message']
        widgets = {
            'receiver': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Type your message...',
                'rows': 3,
            }),
        }