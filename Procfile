release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn --bind 0.0.0.0:${PORT:-8000} hotel.wsgi:application
