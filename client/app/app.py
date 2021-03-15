from flask import Flask, render_template, request, redirect, url_for, make_response
import requests
import json

app = Flask(__name__)


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
        email = request.form['email']
        password = request.form['password']
        role = request.form['options']
        fullname = request.form['name']
        zipcode = request.form['zipcode']

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
                'Content-Type': 'application/x-www-form-urlencoded'
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
        email = request.form['email']
        password = request.form['password']

        res = requests.post(
            'http://localhost:5000/api/v1/login',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
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
            res = requests.get(
                'http://localhost:5000/api/v1/admin',
                headers={
                    'x-auth-token': token
                }
            )

            message = json.loads(res.text)['message']
            if message == "Welcome to Admin Page!":
                response = make_response(render_template('admin/dashboard.html'))
                response.set_cookie('JWT', token)
                return response
            else:
                response = make_response(redirect('/'))
                response.set_cookie('JWT', '')
                response.set_cookie('message', message)
                return response
        elif role == 'donor':
            res = requests.get(
                'http://localhost:5000/api/v1/donor',
                headers={
                    'x-auth-token': token
                }
            )

            message = json.loads(res.text)['message']
            if message == "Welcome to Donor Page!":
                response = make_response(
                    render_template('donor/dashboard.html'))
                response.set_cookie('JWT', token)
                return response
            else:
                response = make_response(redirect('/'))
                response.set_cookie('JWT', '')
                response.set_cookie('message', message)
                return response
        elif role == 'recipient':
            res = requests.get(
                'http://localhost:5000/api/v1/recipient',
                headers={
                    'x-auth-token': token
                }
            )

            message = json.loads(res.text)['message']
            if message == "Welcome to Recipient Page!":
                response = make_response(
                    render_template('recipient/dashboard.html'))
                response.set_cookie('JWT', token)
                return response
            else:
                response = make_response(redirect('/'))
                response.set_cookie('JWT', '')
                response.set_cookie('message', message)
                return response

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
