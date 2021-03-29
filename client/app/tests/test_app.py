import json
import flask
def test_home_page(app, client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Disaster Assistance Management System" in response.data


def test_register_page(app, client):
    
    # Testing GET request
    response = client.get('/register', follow_redirects=True)
    assert response.status_code == 200
    assert b"DAMS Register" in response.data

    # Testing POST request
    data = {
        'email': 'admin@admin.com',
        'password': '123456',
        'name': 'Admin',
        'options': 'admin',
        'zipcode': '52242'
    }
    headers = {
        "Content-Type": "application/form-urlencoded"
    }
    response = client.post(
        '/register', data=data, headers=headers, follow_redirects=True)
    assert response.status_code == 200


def test_login_page(app, client):

    # Testing GET request
    client.set_cookie('localhost', 'JWT', '')
    response = client.get('/login', follow_redirects=True)
    assert response.status_code == 200
    assert b"DAMS Login" in response.data

    # Testing POST request
