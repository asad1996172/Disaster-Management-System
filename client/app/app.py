from flask import Flask, render_template, request, redirect, url_for, make_response
import requests
import json

app = Flask(__name__)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['options']

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
            user = json.loads(res.text)['payload']
            print("JWT Token: ", token)
            response = make_response(redirect(url_for('dashboard')))
            response.set_cookie('JWT', token)
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
