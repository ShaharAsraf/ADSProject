#!/bin/bash

rm db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate --run-syncdb
python3 manage.py createsuperuser
python3 funkcje.py
python3 manage.py loaddata items_final.json