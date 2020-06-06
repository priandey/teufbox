#! /bin/bash
PATH=$PATH:/home/archenior/.pyenv/plugins/pyenv-virtualenv/shims:/home/archenior/.pyenv/shims:~/.pyenv/bin:/home/archenior/.local/share/umake/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
cd ~/PycharmProjects/teufbox/teufboxApp/
exec rhythmbox %U&
(sleep 4; firefox "127.0.0.1:8000")&
exec pipenv run python manage.py runserver
