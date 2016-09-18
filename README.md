django-project-template
=====================


#### Usage ####


#### Getting Started ####

    pip install virtualenv
    virtualenv mysiteenv
    source mysiteenv/bin/activate
    pip install Django==1.6.2

    cd mysite
    (for Windows) easy_install pycrypto-xxx.exe
    (for WIndows) easy_install pywin32-xxx.exe
    pip install -r requirements.txt
    python manage.py syncdb --noinput
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

#### Deployment (nginx, gunicorn, supervisor, virtualenv) ####

* create a new repo (same name as 'mysite') on Bitbucket and push the new created project into it
* customize fabfile.py
```python
    env.repository = 'https://bitbucket.org/myname/myreponame'
    env.hosts = [HOST-SERVER-NAME-OR-IP, ]
    env.user = HOST-USER
    env.key_filename = ["ec2.pem", ]  # PEM file for Aamzon EC2 (optional)
    ...
    env.gunicorn_bind = "127.0.0.1:PORT"  # port for the app instance, e.g. 8100
    ...
    env.nginx_server_name = 'mysite.com'  # Only domain name, without 'www' or 'http://'
```
    
* run test, and (system level and project level) setup on local machine

```
fab app test_configuration
fab app setupsystem
fab app setupproject
```

* manually create (mysql) database and configure local_settings.py on the server

```
$ mysql -u root -p
mysql> CREATE DATABASE dbname;
mysql> GRANT ALL ON dbname.* TO 'dbuser'@'localhost' IDENTIFIED BY 'dbpassword';
mysql> quit
```

* run deployment

```
fab app deploy
```

#### Extra Manual Setup (optional) ####

```
sudo chown -R django site_media
```
