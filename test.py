import os
import sys
import django
import re
from faker import Faker
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Twitter2.settings')
django.setup()
from account.models import User


def create_users(count):
    for i in range(count):
        fake = Faker()
        age = fake.random_int(min=18, max=75)
        name = fake.name()
        first_name = name.split()[0]
        last_name = name.split()[1]
        job = fake.job()
        country = fake.country()
        base_username = re.sub(r'[^a-zA-Z0-9]', '', name.split()[0]).lower()
        username = f"{base_username}{fake.random_int(10, 99)}"
        email = f"{username}@{fake.free_email_domain()}"

        new_user = User(email=email, first_name=first_name, last_name=last_name, password="12345678", location=country, username=username, bio=job)
        new_user.save()

def create_tweets():
    import ollama
    users = User.objects.all()
    for user in users[1:]:
        if user == "Fazlolah Arvand":
            continue

        tweet_count = Faker().random_int(min=1, max=5)

        for i in range(tweet_count):
            tweet_prompt = f"""Your name is {user.get_full_name()} with the username {user.username} your job is {user.bio} You are from {user.location},
            Generate a short and engaging tweet about any random topic. Keep it under 280 characters."""

            response = ollama.chat(model='llava', messages=[{"role": "user", "content": tweet_prompt}])
            tweet_content = response['message']['content']

            user.tweet_set.create(text=tweet_content)

        print(f"{tweet_count} Tweets created for {user.get_full_name()}")

def random_follows():
    users = User.objects.all()

    for user in users:
        following_count = random.randint(4, 20)

        for i in range(following_count):
            following = users[random.randint(0, len(users) - 1)]
            try:
                user.following.create(followed=following)
            except django.db.utils.IntegrityError:
                pass

        print(f"{following_count} random follows created for {user.get_full_name()}")
    print("All done!")

# from core.models import Tweet

# tweets = Tweet.objects.all()

# for tweet in tweets:
#     faz = User.objects.get(username="fazlolah")
#     if tweet.likes.filter(user=faz, tweet=tweet).exists():
#         print(tweet)


# for tweet in tweets:
#     # print(tweet.text)
#     if tweet.text.strip().startswith("\"") and tweet.text.strip().endswith("\""):
#         tweet.text = tweet.text.strip()[1:-1]
#         print(tweet.text)
#         tweet.save()
#     # print(tweet.text)
#     # break

users = User.objects.all()
for user in users:
    if user.username == "fazlolah":
        continue
    print(user.username)
    user.set_password("123456789")
    user.save()