#!/bin/bash
python manage.py write_events events.csv
python manage.py write_hpo hpo.csv
python manage.py write_students students.csv
python manage.py write_attendees attendees.csv

mysql < clear_tables.sql

python manage.py syncdb

python manage.py read_attendees attendees.csv
python manage.py read_students students.csv
python manage.py read_events events.csv
python manage.py read_hpo hpo.csv


