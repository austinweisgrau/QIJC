# Quantum Information Journal Club Website

## Accessing the QIJC web application

A mockup of this website can be found deployed on an [AWS EC2 Instance 
here](http://ec2-54-186-242-58.us-west-2.compute.amazonaws.com). \
The actual deployment is used by a NIST research lab at CU Boulder. \
The app can be launched on a local machine after installing dependencies and executing "flask run" from the command line, then accessing http://localhost:5000. More detailed instructions are below.

## Features

QIJC serves a journal club. Users request accounts from the administrator. Once approved, users submit research paper links. The application scrapes the metadata using the arXiv.org API or users submit the metadata manually if the scraper fails. Users can volunteer to present papers and comment on the papers directly. Submitted papers are periodically emailed out to the full list, voted on by the collective group and archived by vote instance. Users can search through submitted papers by any combination of fields. Users can view each others profiles, which list submitted papers and a point ranking system for engagement. Administrators have access to a management page for changing user permissions or retiring users.

### QIJC is a robust full-stack flask application extensively utilizing many Flask libraries:
* User authentication with Flask-Login
* WTForms with Flask-WTF
* Bootstrap with Flask-Bootstrap
* SQLite with Flask-SQLAlchemy
* Outgoing mail service with Flask-Mail
* Views rendered with HTML, CSS, Bootstrap & Jinja2

## Licensing

## Detailed instructions to run application on local machine:

Clone repo: \
git clone https://github.com/aradox66/QIJC.git \
cd QIJC

Create virtual environmental and install dependencies: \
python3.6 -m venv venv/ \
source venv/bin/activate \
pip install -r requirements.txt

Launch with flask from main folder: \
export FLASK_APP = main.py \
flask run
