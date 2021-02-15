sudo apt update
sudo apt install python3.5
sudo ln -sf /usr/bin/python3.5 /usr/bin/python3
sudo pip3 install Django==2.1
# sudo pip3 install -r requirements.txt

# sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
# sudo nginx -t
# sudo /etc/init.d/nginx restart

# sudo ln -sf /home/box/web/etc/gunicorn-django.conf /etc/gunicorn.d/test-django
# sudo /etc/init.d/gunicorn restart
# sudo gunicorn -b 0.0.0.0:8080 ~/web/hello:app
# sudo gunicorn -b 0.0.0.0:8000 ~/web/ask/ask.wsgi:application

sudo /etc/init.d/nginx stop
sudo python3 ~/web/ask/manage.py runserver 0.0.0.0:80