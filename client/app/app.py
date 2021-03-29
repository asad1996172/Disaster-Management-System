from flask import Flask, render_template, request, redirect, url_for, make_response
import requests
import json

app = Flask(__name__)
json_header = 'application/JSON"'
api_header = 'application/x-www-form-urlencoded'

@app.route('/create_event', methods=['POST', 'GET'])
def create_event():
    if request.method == 'GET':
        return render_template('admin/create_event.html')
    elif request.method == 'POST':
        headers = request.headers
        if headers.get('Content-Type') == json_header:
            data_string = request.get_data()
            form = json.loads(data_string)
        else:
            form = request.form

        event_name = form['event_name']
        disaster_type = form['disaster_type']
        severity = form['severity']
        location = form['location']
        zipcode = form['zipcode']
        event_date = form['event_date']
        if headers.get('Content-Type') == json_header:
            items = form['items']
        else:
            items = form.getlist('mytext[]')
            items = ', '.join(items)
        
        data_payload = {
            'event_name': event_name,
            'disaster_type': disaster_type,
            'severity': severity,
            'location': location,
            'event_date': str(event_date),
            'zipcode': zipcode,
            'items': items
        }
        token = request.cookies.get('JWT')
        res = requests.post(
            'http://localhost:5000/api/v1/create_event',
            headers={
                'Content-Type': api_header,
                'x-auth-token': token
            },
            data=data_payload
        )
        message = json.loads(res.text)['message']

        if message == 'Event Created!':
            response = make_response(redirect('/dashboard'))
            return response
        elif message == "Cannot create event at the moment!" or message == "Event already exists!":
            return render_template('admin/create_event.html', message = message)
        else:
            response = make_response(redirect('/'))
            response.set_cookie('JWT', '')
            response.set_cookie('message', message)
            return response
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if request.method == 'GET':
        response = make_response(redirect(url_for('login')))
        response.set_cookie('JWT', '')
        response.delete_cookie('Name')
        response.delete_cookie('Role')
        response.delete_cookie('Zipcode')
        response.delete_cookie('Email')
        return response

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        headers = request.headers
        if headers.get('Content-Type') == json_header:
            data_string = request.get_data()
            form = json.loads(data_string)
        else:
            form = request.form

        email = form['email']
        password = form['password']
        role = form['options']
        fullname = form['name']
        zipcode = form['zipcode']

        data_payload = {
            'email': email,
            'password': password,
            'fullName': fullname,
            'role': role,
            'zipcode': zipcode
        }
        res = requests.post(
            'http://localhost:5000/api/v1/register',
            headers={
                'Content-Type': api_header,
            },
            data=data_payload
        )
        message = json.loads(res.text)['message']
        response = make_response(redirect('/'))
        response.set_cookie('message', message)
        return response

    else:
        return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        headers = request.headers
        if headers.get('Content-Type') == json_header:
            data_string = request.get_data()
            form = json.loads(data_string)
        else:
            form = request.form
        
        email = form['email']
        password = form['password']

        res = requests.post(
            'http://localhost:5000/api/v1/login',
            headers={
                'Content-Type': api_header
            },
            data={
                'email': email,
                'password': password
            }
        )
        
        message = json.loads(res.text)['message']
        if message == "Email or password does not match!":
            return render_template('login.html', message=message)
        else:
            token = json.loads(res.text)['token']
            user = json.loads(res.text)['payload']['user']
            response = make_response(redirect(url_for('dashboard')))
            response.set_cookie('JWT', token)
            response.set_cookie('Name', user['name'])
            response.set_cookie('Role', user['role'])
            response.set_cookie('Zipcode', user['zipcode'])
            response.set_cookie('Email', user['email'])
            return response

    else:
        token = request.cookies.get('JWT')
        if token=='':
            return render_template('login.html')
        else:
            return redirect(url_for('dashboard'))
    
def admin_dashboard(token):
    res = requests.get(
        'http://localhost:5000/api/v1/admin',
        headers={
                    'x-auth-token': token
                }
    )
    message = json.loads(res.text)['message']
    if message == "Welcome to Admin Page!":
        events = json.loads(res.text)['events']
        parsed_events = []
        for event in events:
            event['event_date'] = event['event_date'].split('T')[0]
            parsed_events.append(event)
        name = request.cookies.get('Name')
        response = make_response(render_template(
            'admin/dashboard.html', name=name, events=parsed_events))
        response.set_cookie('JWT', token)
        return response
    else:
        response = make_response(redirect('/'))
        response.set_cookie('JWT', '')
        response.set_cookie('message', message)
        return response

def donor_dashboard(token):
    res = requests.get(
        'http://localhost:5000/api/v1/donor',
        headers={
                        'x-auth-token': token
                    }
    )

    message = json.loads(res.text)['message']
    if message == "Welcome to Donor Page!":
        name = request.cookies.get('Name')
        response = make_response(
            render_template('donor/dashboard.html', name=name))
        response.set_cookie('JWT', token)
        return response
    else:
        response = make_response(redirect('/'))
        response.set_cookie('JWT', '')
        response.set_cookie('message', message)
        return response

def recipient_dashboard(token):
    res = requests.get(
        'http://localhost:5000/api/v1/recipient',
        headers={
                        'x-auth-token': token
                    }
    )

    message = json.loads(res.text)['message']
    if message == "Welcome to Recipient Page!":
        name = request.cookies.get('Name')
        response = make_response(
            render_template('recipient/dashboard.html', name=name))
        response.set_cookie('JWT', token)
        return response
    else:
        response = make_response(redirect('/'))
        response.set_cookie('JWT', '')
        response.set_cookie('message', message)
        return response

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'GET':
        token = request.cookies.get('JWT')

        if token == '':
            response = make_response(redirect('/'))
            response.set_cookie('JWT', '')
            response.set_cookie('message', 'Only Logged In Users have Access')
            return response
        role = request.cookies.get('Role')
        if role == 'admin':  
            return admin_dashboard(token)
        elif role == 'donor':
            return donor_dashboard(token)
        elif role == 'recipient':
            return recipient_dashboard(token)

@app.route('/')
def dams_homepage():
    res = requests.get(
        'http://localhost:5000/',
        params={})
    
    json.loads(res.text)['status']
    message = request.cookies.get('message')
    response = make_response(render_template('home.html', message=message))
    if 'JWT' not in request.cookies:
        response.set_cookie('JWT', '')
    if 'message' in request.cookies:
        response.set_cookie('message', '')
    return response



if __name__ == '__main__':
    app.run(debug=True, port=5050)
