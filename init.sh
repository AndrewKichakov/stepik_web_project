sudo apt update
sudo apt install python3.9
sudo unlink /usr/bin/python3
sudo ln -s /usr/bin/python3.9 /usr/bin/python3
sudo pip3 install --upgrade pip
sudo pip3 install --upgrade django==2.1
sudo pip3 install --upgrade gunicorn
sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
sudo nginx -t
sudo /etc/init.d/nginx restart
sudo /etc/init.d/gunicorn restart
sudo gunicorn -b 0.0.0.0:8080 ~/web/hello:app
sudo gunicorn -b 0.0.0.0:8000 ~/web/ask.wsgi:application