web: gunicorn index:server --workers 4
worker: celery -A index:celery_instance worker