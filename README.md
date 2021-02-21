# Disaster Assitance Management System (DAMS)
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/) <br>

Python Django based web application with MondoDB for Disaster Assistance Management System (DAMS). This system has 3 user types. Admin, Helpers and Helpees. Admin manages disaster events, helpees register them self to events and helpers provide resources for helpees.


## Table of Contents

* [Features](#Features)
* [Installation](#installation)

## Features

-   Information related to disaster events around the globe
-   Helpees registering to disaster events
-   Donors providing assistance for disaster events
-   Donors pledging to disastr events

## Getting Started

### Setting up Python and Virtual Environment 
> Be sure to have Python 3.7+ installed
Clone this repository
```sh
git clone https://github.com/asad1996172/Disaster-Management-System
```
Download and Install Python3
```
https://www.python.org/download/releases/3.0/
```
Install virtualenv
```
pip3 install virtualenv
```
Create virtual environment 
```
virtualenv -p python3 env
```
Activate virtual environment 
```
source env/bin/activate (For Mac)
env\scripts\activate (For Windows)
```
Check virtual environment 
```
pip -V (Check the path to see if project's env is activated)
```
Install required libraries
```
pip install -r requirements.txt
```

### Installing MongoDB
Install mongodb
```
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/ (For mac)
https://www.mongodb.com/try/download/community?tck=docs_server (for windows)
```
Install MongoDB compass for managing MongoDB
```
https://www.mongodb.com/products/compass
```
> MongoDB compass will automatically be installed in the windows installation
### Running Server
Make db migrations
```
python manage.py makemigrations
```
Migrate DB
```
python manage.py migrate
```
Run Django server
```
python manage.py runserver
```
You should be seeing the following screen, If the setup is successfully completed.

![Startup Screen](https://github.com/asad1996172/Disaster-Management-System/blob/main/django-dams.png)
