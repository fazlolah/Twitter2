from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpForm(UserCreationForm):

    first_name = forms.CharField(
        label="First name",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
    )

    last_name = forms.CharField(
        label="Last name",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'})
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    date_of_birth = forms.DateField(
        label="Date of birth",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date of birth'})
    )

    location = forms.CharField(
        label="Location",
        max_length=1024,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
    )

    gender = forms.ChoiceField(
        label="Gender",
        choices=User.GENDER_CHOICES,  # Assuming GENDER_CHOICES exists in the User model
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    bio = forms.CharField(
        label="Bio",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us about yourself', 'rows': 4}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'gender', 'bio', 'date_of_birth', 'location', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm your password'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label="Username or Email",
        required=True,
        widget=forms.TextInput(attrs={"class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"})
    )

    password = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(attrs={"class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"})
    )

    remember_me = forms.BooleanField(
        label="Remember me",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "h-4 w-4 text-blue-500 border-gray-300 rounded focus:ring-blue-500"})
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        required=True,
        max_length=256,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email"})
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'profile_picture', 'location', 'date_of_birth', 'gender']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }