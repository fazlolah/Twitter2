from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DirectMessage
from .forms import DirectMessageForm
from account.models import User
from django.db import models
from notification.models import Notification
from django.db.models import Max, Q
from django.contrib import messages

@login_required
def send_direct_message(request, receiver_id=None):
    receiver = None
    if receiver_id:
        receiver = get_object_or_404(User, id=receiver_id)

    if request.method == 'POST':
        form = DirectMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            if receiver:
                message.receiver = receiver
            message.save()
            return redirect('view_conversation', user_id=receiver_id)
        else:
            messages.error(request, message="there was an error sending your message.")


@login_required
def view_direct_messages(request):
    # Get all messages where the current user is the sender or receiver
    messages = DirectMessage.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user))
    
    # Create a dictionary to store unique conversations
    conversations = {}

    for message in messages:
        # Determine the other user in the conversation
        if message.sender == request.user:
            other_user = message.receiver
        else:
            other_user = message.sender
        
        # Use a tuple of sorted user IDs as the key to ensure uniqueness
        key = tuple(sorted([request.user.id, other_user.id]))
        
        # Update the conversation with the latest message
        if key not in conversations or message.timestamp > conversations[key]['latest_message'].timestamp:
            conversations[key] = {
                'other_user': other_user,
                'latest_message': message,
            }

    # Convert the dictionary to a list of conversations
    conversation_list = list(conversations.values())

    # Sort conversations by the latest message timestamp
    conversation_list.sort(key=lambda x: x['latest_message'].timestamp, reverse=True)

    return render(request, 'directmessage/all_messages_page.html', {'conversations': conversation_list})

@login_required
def view_conversation(request, user_id):

    # Get all messages where the current user is the sender or receiver
    messages = DirectMessage.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user))
    # Create a dictionary to store unique conversations
    conversations = {}
    for message in messages:
        # Determine the other user in the conversation
        if message.sender == request.user:
            other_user = message.receiver
        else:
            other_user = message.sender
        # Use a tuple of sorted user IDs as the key to ensure uniqueness
        key = tuple(sorted([request.user.id, other_user.id]))
        # Update the conversation with the latest message
        if key not in conversations or message.timestamp > conversations[key]['latest_message'].timestamp:
            conversations[key] = {
                'other_user': other_user,
                'latest_message': message,
            }
    # Convert the dictionary to a list of conversations
    conversation_list = list(conversations.values())
    # Sort conversations by the latest message timestamp
    conversation_list.sort(key=lambda x: x['latest_message'].timestamp, reverse=True)

    other_user = get_object_or_404(User, id=user_id)
    messages = DirectMessage.objects.filter(
        models.Q(sender=request.user, receiver=other_user) |
        models.Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')
    # Mark messages as read when viewed
    unread_messages = messages.filter(receiver=request.user, is_read=False)
    unread_messages.update(is_read=True)

    if user_id:
        receiver = get_object_or_404(User, id=user_id)
    form = DirectMessageForm(initial={'receiver': receiver} if receiver else None)


    return render(request, 'directmessage/chat_page.html', {
        'messages': messages,
        'other_user': other_user,
        'conversations': conversation_list,
        'form':form,
    })