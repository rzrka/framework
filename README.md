uwsgi --http :8000 --wsgi-file main.py
kill -9 $(lsof -t -i:8000)
