try:
    from webbrowser import open 
    open('http://127.0.0.1:8000')
    from os import system
    system("python manage.py runserver")
except KeyboardInterrupt:
    pass