sudo /etc/init.d/mysql start
mysql -u root -e "CREATE DATABASE djbase;"
mysql -u root -e "CREATE USER 'django'@'localhost' IDENTIFIED BY 'pass123';"
mysql -u root -e "GRANT ALL ON djbase.* TO 'django'@'localhost';"
mysql -u root -e "FLUSH PRIVILEGES;"