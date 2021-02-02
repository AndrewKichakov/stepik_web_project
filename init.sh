sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
sudo nginx -t
sudo /etc/init.d/nginx restart
sudo ln -sf /home/box/web/etc/gunicorn-django.conf /etc/gunicorn.d/test-django
sudo /etc/init.d/gunicorn restart
sudo gunicorn -b 0.0.0.0:8080 ~/web/hello:app
sudo gunicorn -b 0.0.0.0:8000 ~/web/ask/ask.wsgi:application