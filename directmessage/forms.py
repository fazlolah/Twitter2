from django import forms
from .models import DirectMessage

class DirectMessageForm(forms.ModelForm):
    class Meta:
        model = DirectMessage
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={
                'class': 'max-w mx-auto flex-1 border border-gray-300 rounded-full px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Type your message...',
            }),
        }