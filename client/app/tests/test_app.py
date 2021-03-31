import json
import requests

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
        "Content-Type": "application/JSON"
    }
    response = client.post(
        '/register', data=json.dumps(data), headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert b"Thanks for registering" in response.data
    
    res = requests.post(
        'http://localhost:5000/api/v1/delete_user',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data={'email': 'admin@admin.com'}
    )
    message = json.loads(res.text)['message']
    assert message == "User deleted successfully"

def test_login_page(app, client):

    # Testing GET request
    client.set_cookie('localhost', 'JWT', '')
    response = client.get('/login', follow_redirects=True)
    assert response.status_code == 200
    assert b"DAMS Login" in response.data

    # Testing POST request
    data = {
        'email': 'admin@admin.com',
        'password': '123456',
        'name': 'Admin',
        'options': 'admin',
        'zipcode': '52242'
    }
    headers = {
        "Content-Type": "application/JSON"
    }
    response = client.post(
        '/register', data=json.dumps(data), headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert b"Thanks for registering" in response.data

    login_user_data = {
        'email': 'admin@admin.com',
        'password': '123456'
    }

    login_wrong_user_data = {
        'email': 'random@admin.com',
        'password': '123456'
    }

    response = client.post(
        '/login', data=json.dumps(login_wrong_user_data), headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert b"Email or password does not match!" in response.data

    response = client.post(
        '/login', data=json.dumps(login_user_data), headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert b"Admin" in response.data

    res = requests.post(
        'http://localhost:5000/api/v1/delete_user',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data={'email': 'admin@admin.com'}
    )
    message = json.loads(res.text)['message']
    assert message == "User deleted successfully"

def test_logout(app, client):
    
    data = {
        'email': 'admin@admin.com',
        'password': '123456',
        'name': 'Admin',
        'options': 'admin',
        'zipcode': '52242'
    }
    headers = {
        "Content-Type": "application/JSON"
    }
    response = client.post(
        '/register', data=json.dumps(data), headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert b"Thanks for registering" in response.data

    login_user_data = {
        'email': 'admin@admin.com',
        'password': '123456'
    }

    response = client.post(
        '/login', data=json.dumps(login_user_data), headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert b"Admin" in response.data

    response = client.get(
        '/logout', data=json.dumps(login_user_data), headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert b"DAMS Login" in response.data

    res = requests.post(
        'http://localhost:5000/api/v1/delete_user',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data={'email': 'admin@admin.com'}
    )
    message = json.loads(res.text)['message']
    assert message == "User deleted successfully"

def test_dashboard(app, client):
    # Testing GET request
    client.set_cookie('localhost', 'JWT', '')
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b"Only Logged In Users have Access" in response.data

def test_donor_dashboard(app, client):
    # Testing POST request
    data = {
        'email': 'donor@donor.com',
        'password': '123456',
        'name': 'Donor',
        'options': 'donor',
        'zipcode': '52242'
    }
    headers = {
        "Content-Type": "application/JSON"
    }
    response = client.post(
        '/register', data=json.dumps(data), headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert b"Thanks for registering" in response.data

    login_user_data = {
        'email': 'donor@donor.com',
        'password': '123456'
    }

    response = client.post(
        '/login', data=json.dumps(login_user_data), headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert b"Donor" in response.data

    res = requests.post(
        'http://localhost:5000/api/v1/delete_user',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data={'email': 'donor@donor.com'}
    )
    message = json.loads(res.text)['message']
    assert message == "User deleted successfully"

def test_recipient_dashboard(app, client):
    # Testing POST request
    data = {
        'email': 'recipient@recipient.com',
        'password': '123456',
        'name': 'Recipient',
        'options': 'recipient',
        'zipcode': '52242'
    }
    headers = {
        "Content-Type": "application/JSON"
    }
    response = client.post(
        '/register', data=json.dumps(data), headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert b"Thanks for registering" in response.data

    login_user_data = {
        'email': 'recipient@recipient.com',
        'password': '123456'
    }

    response = client.post(
        '/login', data=json.dumps(login_user_data), headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert b"Recipient" in response.data

    resource_data = {
        'event_name': 'Katrina',
        'items': 'Cash, Food',
        'Cash': '10',
        'Food': '10'
    }
    response = client.post(
        '/request_resources', data=json.dumps(resource_data), headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert b"Recipient" in response.data
    
    res = requests.post(
        'http://localhost:5000/api/v1/delete_user',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data={'email': 'recipient@recipient.com'}
    )
    message = json.loads(res.text)['message']
    assert message == "User deleted successfully"

def test_create_event(app, client):
    data = {
        'email': 'admin@admin.com',
        'password': '123456',
        'name': 'Admin',
        'options': 'admin',
        'zipcode': '52242'
    }
    headers = {
        "Content-Type": "application/JSON"
    }
    response = client.post(
        '/register', data=json.dumps(data), headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert b"Thanks for registering" in response.data

    login_user_data = {
        'email': 'admin@admin.com',
        'password': '123456'
    }

    response = client.post(
        '/login', data=json.dumps(login_user_data), headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert b"Admin" in response.data
    
    # Testing GET request
    response = client.get('/create_event', follow_redirects=True)
    assert response.status_code == 200
    assert b"Create Disaster Event" in response.data

    # Testing POST request
    data_payload = {
        'event_name': 'Katrina',
        'disaster_type': 'Hurricane',
        'severity': 'extreme',
        'location': 'US',
        'event_date': '2006-01-01',
        'zipcode': '52245',
        'items': ''
    }
    response = client.post(
        '/create_event', data=json.dumps(data_payload), headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert b"Katrina" in response.data

    res = requests.post(
        'http://localhost:5000/api/v1/delete_event',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data={'event_name': 'Katrina'}
    )
    message = json.loads(res.text)['message']
    assert message == "Event deleted successfully"
    
    res = requests.post(
        'http://localhost:5000/api/v1/delete_user',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data={'email': 'admin@admin.com'}
    )
    message = json.loads(res.text)['message']
    assert message == "User deleted successfully"
