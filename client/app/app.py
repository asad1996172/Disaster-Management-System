from flask import Flask, render_template, request, redirect
import requests
import json

app = Flask(__name__)


@app.route('/admin_login', methods=['POST', 'GET'])
def admin_login():
    if request.method == 'POST':
        pass
    else:
        return render_template('login.html')
    

@app.route('/')
def dams_homepage():
    res = requests.get(
        'http://localhost:5000/',
        params={})
    
    status = json.loads(res.text)['status']
    
    return render_template('home.html', status=status)


if __name__ == '__main__':
    app.run(debug=True, port=5050)
