from flask import Flask, render_template, request, redirect, url_for, make_response
import requests
import json

app = Flask(__name__)
json_header = 'application/JSON'
api_header = 'application/x-www-form-urlencoded'

def updating_matching(req_id, don_id):
    token = request.cookies.get('JWT')
    pledges = requests.get(
        'http://localhost:5000/api/v1/get_pledges',
        headers={
            'x-auth-token': token
        }
    )
    pledges = json.loads(pledges.text)['pledges']

    res = requests.get(
        'http://localhost:5000/api/v1/donor',
        headers={
            'x-auth-token': token
        }
    )

    donation_requests = json.loads(res.text)['requests']
    req_request = None
    for don_request in donation_requests:
        if int(don_request['id']) == int(req_id):
            don_request['item_quantities'] = don_request['item_quantities'].split(
                '|')
            don_request['item_quantities'] = [
                tuple(item_quan.split(':')) for item_quan in don_request['item_quantities']]
            don_request['item_quantities'] = dict(don_request['item_quantities'])
            req_request = don_request
        
    req_pledge = None    
    for pledge in pledges:
        if int(pledge['id']) == int(don_id):
            pledge['item_quantities'] = pledge['item_quantities'].split(
                '|')
            pledge['item_quantities'] = [
                tuple(item_quan.split(':')) for item_quan in pledge['item_quantities']]
            try:
                pledge['item_quantities'] = dict(
                    pledge['item_quantities'])
            except Exception as e:
                continue
            req_pledge = pledge

    print('Request Data: ', req_request)
    print('Pledge Data: ', req_pledge)
    don_request = req_request
    pledge = req_pledge
    
    updated = False
    for item in don_request['item_quantities']:
        if (item in pledge['item_quantities']) and (int(pledge['item_quantities'][item]) > 0) and (int(don_request['item_quantities'][item]) > 0):
            updated = True
            don_amount = int(don_request['item_quantities'][item])
            pledge_amount = int(pledge['item_quantities'][item])

            don_request['item_quantities'][item] = str(
                don_amount - pledge_amount)

            pledge['item_quantities'][item] = str(
                pledge_amount - don_amount)
    if updated:
        new_pledge_item_quan = []
        for item in pledge['item_quantities']:
            if int(pledge['item_quantities'][item]) > 0:
                new_pledge_item_quan.append(
                    item+":"+pledge['item_quantities'][item])
        new_pledge_item_quan = '|'.join(new_pledge_item_quan)
        data_payload = {
            'id': pledge['id'],
            'item_quantities': new_pledge_item_quan
        }
        res = requests.post(
            'http://localhost:5000/api/v1/update_pledge',
            headers={
                'Content-Type': api_header,
                'x-auth-token': token
            },
            data=data_payload
        )

        new_donation_item_quan = []
        for item in don_request['item_quantities']:
            if int(don_request['item_quantities'][item]) > 0:
                new_donation_item_quan.append(
                    item+":"+don_request['item_quantities'][item])
        new_donation_item_quan = '|'.join(new_donation_item_quan)

        data_payload = {
            'event_name': don_request['event_name'],
            'donor_email': request.cookies.get('Email'),
            'recipient_email': don_request['email'],
            'items': new_donation_item_quan
        }
        res = requests.post(
            'http://localhost:5000/api/v1/make_donation',
            headers={
                'Content-Type': api_header,
                'x-auth-token': token
            },
            data=data_payload
        )

@app.route('/match/<req_id>/<don_id>', methods=['GET', 'POST'])
def match(req_id, don_id):
    updating_matching(req_id, don_id)
    response = make_response(redirect('/manual_matching'))
    return response

@app.route('/manual_matching', methods=['GET', 'POST'])
def manual_matching():
    if request.method == 'GET':
        token = request.cookies.get('JWT')
        res = requests.get(
            'http://localhost:5000/api/v1/donor',
            headers={
                'x-auth-token': token
            }
        )

        pledges = requests.get(
            'http://localhost:5000/api/v1/get_pledges',
            headers={
                'x-auth-token': token
            }
        )
        pledges = json.loads(pledges.text)['pledges']
        parsed_pledges = []
        for pledge in pledges:
            if pledge['item_quantities'] != '':
                pledge['raw_item_quantities'] = pledge['item_quantities']
                pledge['item_quantities'] = pledge['item_quantities'].split('|')
                pledge['item_quantities'] = [
                    item_quan.split(':') for item_quan in pledge['item_quantities'] if int(item_quan.split(':')[1]) > 0]
                parsed_pledges.append(pledge)

        message = json.loads(res.text)['message']
        if message == "Welcome to Donor Page!":
            name = request.cookies.get('Name')
            donation_requests = json.loads(res.text)['requests']
            parsed_requests = []
            for don_request in donation_requests:
                if don_request['item_quantities'] != '':
                    don_request['raw_item_quantities'] = don_request['item_quantities']
                    don_request['item_quantities'] = don_request['item_quantities'].split(
                        '|')
                    print(don_request['item_quantities'])
                    don_request['item_quantities'] = [
                        item_quan.split(':') for item_quan in don_request['item_quantities'] if int(item_quan.split(':')[1]) > 0]
                    parsed_requests.append(don_request)

            response = make_response(render_template(
                'admin/manual_matching.html', name=name, donation_requests=parsed_requests, pledges=parsed_pledges))
            return response

@app.route('/edit_event/<event_name>', methods=['GET', 'POST'])
def edit_event(event_name):
    if request.method == 'GET':
        data_payload = {
            'event_name': event_name
        }
        token = request.cookies.get('JWT')
        res = requests.get(
            'http://localhost:5000/api/v1/get_event',
            headers={
                'Content-Type': api_header,
                'x-auth-token': token
            },
            data=data_payload
        )
        message = json.loads(res.text)['message']
        event_details = json.loads(res.text)['event_details']
        event_details['event_date'] = event_details['event_date'].split('T')[0]
        event_details['existing_items'] = ''
        for item in event_details['items'].split(', '):
            event_details['existing_items'] += '<div class="input-group mb-3"> \
                        <div class="input-group-prepend"> \
                            <span class="input-group-text remove_field" id="basic-addon1"><a style="color: red; font-size: 1.5em;" class="fas fa-trash"></a></span> \
                        </div> \
                        <input type="text" class="form-control form-control-user" placeholder="Item name ..." name="mytext[]" value="'+item+'" required> \
                        </div>'
        print(event_details)
        
        response = make_response(render_template(
            'admin/edit_event.html', event=event_details))
        return response

    if request.method == 'POST':
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
            'http://localhost:5000/api/v1/edit_event',
            headers={
                'Content-Type': api_header,
                'x-auth-token': token
            },
            data=data_payload
        )
        message = json.loads(res.text)['message']
        
        response = make_response(redirect('/dashboard'))
        return response

@app.route('/expire_event/<event_name>', methods=['GET'])
def expire_event(event_name):
    if request.method == 'GET':
        
        data_payload = {
            'event_name': event_name
        }
        token = request.cookies.get('JWT')
        res = requests.post(
            'http://localhost:5000/api/v1/expire_event',
            headers={
                'Content-Type': api_header,
                'x-auth-token': token
            },
            data=data_payload
        )
        message = json.loads(res.text)['message']
        response = make_response(redirect('/dashboard'))
        return response

@app.route('/pledge', methods=['POST', 'GET'])
def pledge():
    if request.method == 'GET':
        return render_template('donor/pledge.html')
    elif request.method == 'POST':
        headers = request.headers
        form = request.form
        if headers.get('Content-Type') == json_header:
            items = form['items']
            amounts = form['amounts']
        else:
            items = form.getlist('mytext[]')
            amounts = form.getlist('amounts[]')

        pledge=[]
        for item, amount in zip(items, amounts):
            pledge.append(item+":"+amount)
        pledge = '|'.join(pledge)
        data_payload = {
            'email': request.cookies.get('Email'),
            'item_quantities': pledge
        }
        
        token = request.cookies.get('JWT')
        res = requests.post(
            'http://localhost:5000/api/v1/pledge_resources',
            headers={
                'Content-Type': api_header,
                'x-auth-token': token
            },
            data=data_payload
        )
        message = json.loads(res.text)['message']

        response = make_response(redirect('/dashboard'))
        response.set_cookie('message_donor', message)
        return response

@app.route('/make_donation', methods=['POST'])
def make_donation():
    if request.method == 'POST':
        headers = request.headers
        if headers.get('Content-Type') == json_header:
            data_string = request.get_data()
            form = json.loads(data_string)
        else:
            form = request.form

        data_payload = {
            'event_name': form['event_name'],
            'donor_email': request.cookies.get('Email'),
            'recipient_email': form['recipient_email'],
            'items': []
        }

        items = form['items_quantities']
        
        for item in items.split('|'):
            try:
                item = item.strip().split(':')
            
                item_name = item[0].strip()
                item_required_quantity = item[1].strip()
                give_quantity = form[item_name]
                
                data_payload['items'].append(
                    item_name + ":" + str(int(item_required_quantity) - int(give_quantity)))
            except Exception as e:
                print(e)
        
        data_payload['items'] = '|'.join(data_payload['items'])
        print(data_payload)
        token = request.cookies.get('JWT')
        res = requests.post(
            'http://localhost:5000/api/v1/make_donation',
            headers={
                'Content-Type': api_header,
                'x-auth-token': token
            },
            data=data_payload
        )
        message = json.loads(res.text)['message']
        
        response = make_response(redirect('/dashboard'))
        response.set_cookie('message_donor', message)
        return response

@app.route('/request_resources', methods=['POST'])
def request_resources():
    if request.method == 'POST':
        headers = request.headers
        if headers.get('Content-Type') == json_header:
            data_string = request.get_data()
            form = json.loads(data_string)
        else:
            form = request.form

        data_payload = {
            'event_name': form['event_name'],
            'email': request.cookies.get('Email'),
            'items': []
        }

        items = form['items']
        for item in items.split(', '):
            quantity = form[item]
            data_payload['items'].append(item + ":" + str(quantity))
        
        data_payload['item_quantities'] = '|'.join(data_payload['items'])
        
        token = request.cookies.get('JWT')
        res = requests.post(
            'http://localhost:5000/api/v1/request_resources',
            headers={
                'Content-Type': api_header,
                'x-auth-token': token
            },
            data=data_payload
        )
        message = json.loads(res.text)['message']

        response = make_response(redirect('/dashboard'))
        response.set_cookie('message_recipient', message)
        return response    

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

def update_pledges(token):
    pledges = requests.get(
        'http://localhost:5000/api/v1/get_pledges',
        headers={
            'x-auth-token': token
        }
    )
    pledges = json.loads(pledges.text)['pledges']

    res = requests.get(
        'http://localhost:5000/api/v1/donor',
        headers={
            'x-auth-token': token
        }
    )

    donation_requests = json.loads(res.text)['requests']
    for don_request in donation_requests:
        print(don_request)
        don_request['item_quantities'] = don_request['item_quantities'].split('|')
        don_request['item_quantities'] = [
            tuple(item_quan.split(':')) for item_quan in don_request['item_quantities']]
        don_request['item_quantities'] = dict(don_request['item_quantities'])
        for pledge in pledges:
            pledge['item_quantities'] = pledge['item_quantities'].split(
                '|')
            pledge['item_quantities'] = [
                tuple(item_quan.split(':')) for item_quan in pledge['item_quantities']]
            try:
                pledge['item_quantities'] = dict(
                    pledge['item_quantities'])
            except Exception as e:
                continue
            
            updated=False
            for item in don_request['item_quantities']:
                if (item in pledge['item_quantities']) and (int(pledge['item_quantities'][item]) > 0) and (int(don_request['item_quantities'][item]) > 0):
                    updated=True
                    don_amount = int(don_request['item_quantities'][item])
                    pledge_amount = int(pledge['item_quantities'][item])
                    
                    don_request['item_quantities'][item] = str(
                        don_amount - pledge_amount)
                    
                    pledge['item_quantities'][item] = str(
                        pledge_amount - don_amount)
            if updated:
                new_pledge_item_quan = []
                for item in pledge['item_quantities']:
                    if int(pledge['item_quantities'][item]) > 0:
                        new_pledge_item_quan.append(
                            item+":"+pledge['item_quantities'][item])
                new_pledge_item_quan = '|'.join(new_pledge_item_quan)
                data_payload = {
                    'id': pledge['id'],
                    'item_quantities': new_pledge_item_quan
                }
                res = requests.post(
                    'http://localhost:5000/api/v1/update_pledge',
                    headers={
                        'Content-Type': api_header,
                        'x-auth-token': token
                    },
                    data=data_payload
                )

                new_donation_item_quan = []
                for item in don_request['item_quantities']:
                    if int(don_request['item_quantities'][item]) > 0:
                        new_donation_item_quan.append(
                            item+":"+don_request['item_quantities'][item])
                new_donation_item_quan = '|'.join(new_donation_item_quan)
                
                data_payload = {
                    'event_name': don_request['event_name'],
                    'donor_email': request.cookies.get('Email'),
                    'recipient_email': don_request['email'],
                    'items': new_donation_item_quan
                }
                res = requests.post(
                    'http://localhost:5000/api/v1/make_donation',
                    headers={
                        'Content-Type': api_header,
                        'x-auth-token': token
                    },
                    data=data_payload
                )
                update_pledges(token)
        
def donor_dashboard(token, display_message=""):
    # update_pledges(token)
    res = requests.get(
        'http://localhost:5000/api/v1/donor',
        headers={
                        'x-auth-token': token
                    }
    )
    message = json.loads(res.text)['message']
    if message == "Welcome to Donor Page!":
        name = request.cookies.get('Name')
        donation_requests = json.loads(res.text)['requests']
        parsed_requests = []
        for don_request in donation_requests:
            if don_request['item_quantities'] != '':
                don_request['raw_item_quantities'] = don_request['item_quantities']
                don_request['item_quantities'] = don_request['item_quantities'].split('|')
                don_request['item_quantities'] = [
                    item_quan.split(':') for item_quan in don_request['item_quantities'] if int(item_quan.split(':')[1]) > 0]
                parsed_requests.append(don_request)

        response = make_response(
            render_template('donor/dashboard.html', name=name, donation_requests=parsed_requests, message=display_message))
        response.set_cookie('JWT', token)
        return response
    else:
        response = make_response(redirect('/'))
        response.set_cookie('JWT', '')
        response.set_cookie('message', message)
        return response

def recipient_dashboard(token, display_message=""):
    res = requests.get(
        'http://localhost:5000/api/v1/recipient',
        headers={
                        'x-auth-token': token
                    }
    )

    message = json.loads(res.text)['message']
    if message == "Welcome to Recipient Page!":
        events = json.loads(res.text)['events']
        parsed_events = []
        for event in events:
            event['item_names'] = event['items'].split(', ')
            event['event_date'] = event['event_date'].split('T')[0]
            parsed_events.append(event)
        name = request.cookies.get('Name')
        response = make_response(
            render_template('recipient/dashboard.html', name=name, events=parsed_events, message=display_message))
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
            if 'message_donor' in request.cookies:
                message = request.cookies.get('message_donor')
            else:
                message=""
            return donor_dashboard(token, message)
        elif role == 'recipient':
            if 'message_recipient' in request.cookies:
                message = request.cookies.get('message_recipient')
            else:
                message = ""
            return recipient_dashboard(token, message)

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
