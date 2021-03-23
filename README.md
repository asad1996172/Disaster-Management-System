# Disaster Assitance Management System (DAMS)


Python Flask and NodeJS based web application with MySQL for Disaster Assistance Management System (DAMS). This system has 3 user types. Admin, Helpers and Helpees. Admin manages disaster events, helpees register them self to events and helpers provide resources for helpees.


## Table of Contents

* [Features](#Features)
* [Installation](#installation)

## Features

-   Information related to disaster events around the globe
-   Helpees registering to disaster events
-   Donors providing assistance for disaster events
-   Donors pledging to disastr events

## Getting Started
Clone this repository
```sh
git clone https://github.com/asad1996172/Disaster-Management-System
```

To enable administrator acces in VScode for Windows run ```Set-ExecutionPolicy Unrestricted```

### Setting up Server-side
1) Install NodeJS
2) Install XAMPP: ```https://sourceforge.net/projects/xampp/files/XAMPP%20Mac%20OS%20X/8.0.2/```
3) Run mysql server and apache server from Xampp Control Manager
4) Go to server directory and run ```npm install``` to install node modules
5) Run ```npm run server``` to start backend server
6) Run ```npm run test``` to run tests and generate coverage report

### Setting up Client-side
1) Go to client directory and create virtualenv using Python 3.6.5 ```virtualenv -p python3 env```
2) Activate virtual environment ```source env/bin/activate``` For Mac and ```.\env\Scripts\activate``` For Windows
3) Install required python libraries ```pip install -r requirements.txt```
4) Run client server ```python app.py```
7) Run python tests and generate coverage report ```pytest --cov=app --cov-report=html:coverage```


