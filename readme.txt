To launch app:

Clone repo:
git clone https://github.com/aradox66/QIJC.git
cd QIJC

Create virtual environmental and install dependencies:
python3.6 -m venv venv/
source venv/bin/activate
pip install -r requirements.txt

Launch with flask from main folder:
flask run

If it doesn't work, try:
export FLASK_APP = main.py
flask run

##################################################
6.3:
currently experimenting with loading the archived database from 2017
qijc17_copy.sqlite is the experimental adapted archive
qijc17_my.sql is the original dump
database is set in config.py
