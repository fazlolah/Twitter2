from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from core.models import Tweet, Follow, Like, User, Retweet, Tag, Comment
from core.forms import TweetForm, CommentForm
from notification.models import Notification
from django.http import JsonResponse
from django.db.models import Count

def home_feed(request):
    tweet_form = TweetForm(request.POST, request.FILES)

    if not request.user.is_authenticated:
        tweets = Tweet.objects.all().order_by('-created_at')
        return render(request, 'core/home_feed.html', {'user':request.user, 'tweet_form': tweet_form, 'tweets': tweets})

    # Get the users that the current user follows
    followed_users = User.objects.filter(followers__follower=request.user)
    # Get tweets from followed users, ordered by creation time
    tweets = Tweet.objects.filter(author__in=followed_users).order_by('-created_at')

    return render(request, 'core/home_feed.html', {'user':request.user, 'tweet_form': tweet_form, 'tweets': tweets})

def explore_feed(request):

    # Get the most trending tag in a single query
    trending_tags = Tag.objects.annotate(tweet_count=Count('tweets')).order_by('-tweet_count')[0:5]

    return render(request, 'core/explore.html', {'trending_tags': trending_tags})

def explore_tag(request, tag):
    tag = tag.lstrip('#')  # Remove '#' prefix if present
    tag = get_object_or_404(Tag, slug=tag.lower())
    tweets = tag.tweets.all().order_by('-created_at')

    return render(request, 'core/explore_tag.html', {'tweets': tweets})

def view_tweet(request, username=None, tweet_id=None):
    comment_form = CommentForm()
    tweet = Tweet.objects.get(id=tweet_id,)
    return render(request, 'core/single_tweet_page.html', {'tweet': tweet, 'comment_form': comment_form})

@login_required
def post_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.author = request.user
            tweet.save()
            return redirect('home')
    else:
        return redirect('home')
    return render(request, 'post_tweet.html', {'form': form})

@login_required
def post_reply(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    parent_comment = None

    # Check if this is a reply to another comment
    # if parent_comment_id:
    #     parent_comment = get_object_or_404(Comment, id=parent_comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = tweet
            comment.parent = parent_comment  # Set the parent comment if it's a reply
            comment.save()
            return redirect('view_tweet', tweet_id=tweet.id)

@login_required
def follow_user(request, user_id):
    user_to_follow = User.objects.get(id=user_id)
    followed, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)

    if created:

        Notification.objects.create(
                sender_id=request.user.id,
                user=user_to_follow,
                type="follow",
                tweet_id=None  # Link to the tweet
        )

    return redirect('user_profile', username=user_to_follow.username)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = User.objects.get(id=user_id)
    Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
    return redirect('user_profile', username=user_to_unfollow.username)

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

        Notification.objects.create(
            sender_id=request.user.id,
            user=tweet.author,
            type="like",
            tweet_id=tweet  # Link to the tweet
        )

    return JsonResponse({'liked': liked, 'like_count': tweet.like_count()})

@login_required
def retweet_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    retweet, created = Retweet.objects.get_or_create(user=request.user, tweet=tweet)

    if not created:
        retweet.delete()
        retweet = False
    else:
        retweet = True

        Notification.objects.create(
            sender_id=request.user.id,
            user=tweet.author,
            type="retweet",
            tweet_id=tweet  # Link to the tweet
        )

    return JsonResponse({'retweeted': retweet, 'retweet_count': tweet.retweet_count()})

@login_required
def delete_tweet(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    
    # Ensure the user can only delete their own tweets
    if tweet.author == request.user:
        tweet.delete()
    
    return redirect('home')

@login_required
def edit_tweet(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    if tweet.author != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'edit_tweet.html', {'form': form})

def search(request):
    query = request.GET.get('q')
    
    if query:
        users = User.objects.filter(username__icontains=query)
        tweets = Tweet.objects.filter(text__icontains=query)
    else:
        users = User.objects.none()
        tweets = Tweet.objects.none()
    
    return render(request, 'core/search_results.html', {
        'users': users,
        'tweets': tweets,
        'query': query
    })

