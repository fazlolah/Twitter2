from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from account.forms import ForgotPasswordForm, LoginForm, SignUpForm, UserProfileForm
from account.models import User
from django.contrib import messages

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username_or_email = login_form.cleaned_data["username_or_email"]
            password = login_form.cleaned_data["password"]
            remember_me = login_form.cleaned_data["remember_me"]

            user = authenticate(request, username=username_or_email, password=password)
            if user:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires on browser close
                return redirect("user_profile", username=user.username)
            else:
                messages.error(request, 'Invalid username/email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        login_form = LoginForm()

    context = {'login_form': login_form}
    return render(request, "account/login.html", context=context)


def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'There were errors in your submission. Please try again.')
    else:
        form = SignUpForm()

    context = {'signup_form': form}
    return render(request, 'account/signup.html', context=context)


def forgotpassword_page(request):
    if request.method == "POST":
        forgotpass_form = ForgotPasswordForm(request.POST)
        if forgotpass_form.is_valid():
            # Add logic to send a password reset email
            email = forgotpass_form.cleaned_data['email']
            # Example: Send an email (you need to implement email functionality)
            messages.success(request, f"A password reset link has been sent to {email}.")
            return redirect("login")
        else:
            messages.error(request, "Invalid email address.")

    forgotpass_form = ForgotPasswordForm()
    context = {'forgotpass_form': forgotpass_form}  # Fixed key typo
    return render(request, "account/forgot-password.html", context=context)


def user_account(request):
    if request.user.is_authenticated:
        username = request.user
        context = {"username":username}
        return render(request, "account/profile.html", context)
    return redirect('login')
    

def user_logout(request):
    logout(request)
    return redirect('login')


def all_users(request):
    users = User.objects.all()
    context = {'users':users}
    return render(request=request, template_name='account/index.html', context=context)


def user_profile(request, username):
    username = username.lstrip('@')  # Remove '@' prefix if present
    user = get_object_or_404(User, username=username)
    context = {'user': user,
               'user_tweets': user.tweet_set.all().order_by('-created_at')}
    return render(request, 'account/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', user_id=request.user.id)
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})