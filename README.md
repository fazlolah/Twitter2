# Twitter2

A Twitter-like social media platform built with Django. This project implements core Twitter functionalities including tweets, retweets, follows, likes, direct messages, and notifications.

## Features

- **User Management**
  - Custom User Authentication
  - User Registration and Login
  - Password Recovery System
  - Profile Management
  - Profile Editing

- **Functionalities**
  - Tweet Creation and Management
  - Like System
  - Comment System
  - Follow/Unfollow Users
  - Hashtag Support (#)
  - Mention Support (@)

- **Additional Features**
  - Direct Messaging System
  - Real-time Notifications
  - Media File Support
  - Tag System

## Stack

- Python 3
- Django
- SQLite3
- HTML/CSS
- JavaScript
- Tailwind CSS

## Usage

Run the development server
```bash
python manage.py runserver
```

Or use the `run_server.py` script which will automatically open the website in your default browser:
```bash
python run_server.py
```

## Apps

- `account/` - User authentication and profile management
- `core/` - Main application features (tweets, follows, etc.)
- `directmessage/` - Private messaging system
- `notification/` - User notification system
- `static/` - Static files (CSS, JavaScript, etc.)
- `templates/` - HTML templates
- `media/` - User-uploaded files

## URLs

- Home: `/`
- Admin: `/admin/`
- User Profiles: `/user/{username}`
- Notifications: `/notifications/`
- Direct Messages: `/messages/`

## TODO
 - retweets
 - editing and removing tweets
 - better front-end
 - block and report functionality
 - keyword and sentiment extracion
