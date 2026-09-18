from src.schemas import UserResponse

def test_register_success(client):
    data = {
        'email': 'testemail123@gmail.com',
        'password': 'testpassword',
        'first_name': 'testfirstname',
        'last_name': 'testlastname'
    }

    res = client.post('/auth/register', json=data)
    user = UserResponse(**res.json())

    assert res.status_code == 201
    assert res.json()['email'] == 'testemail123@gmail.com'

def test_login_success(client, registered_user):
    data = {
        'username': registered_user['email'],
        'password': registered_user['password']
    }

    res = client.post('/auth/login', data=data)
    assert res.status_code == 200
    assert res.json().get('access_token') is not None
    assert res.cookies.get('refresh_token') is not None

def test_logout_success(client, logged_in):
    access_token, refresh_token = logged_in

    res = client.post(
        '/auth/logout',
        cookies={'refresh_token': refresh_token},
        headers={'Authorization': 'Bearer ' + access_token}
    )

    assert res.status_code == 204
    assert res.cookies.get('refresh_token') is None

def test_refresh_success(client, logged_in):
    access_token, refresh_token = logged_in

    res = client.post(
        '/auth/refresh',
        cookies={'refresh_token': refresh_token},
        headers={'Authorization': 'Bearer ' + access_token}
    )
    assert res.status_code == 200
    assert res.json().get('access_token') is not None
    assert res.cookies.get('refresh_token') is not None

def test_register_failure_duplicate_email(client, registered_user):
    data = {
        'email': 'registeredemail123@gmail.com',
        'password': 'testpassword',
        'first_name': 'testfirstname',
        'last_name': 'testlastname'
    }

    res = client.post('/auth/register', json=data)
    assert res.status_code == 409
    assert res.json().get('detail') == 'User with that email already exists'

def test_login_failure_invalid_credentials(client):
    data = {
        'username': 'testusername',
        'password': 'somepassword'
    }

    res = client.post('/auth/login', data=data)
    assert res.status_code == 400
    assert res.json().get('detail') == 'Invalid credentials'

def test_auth_failure_missing_access_token(client):
    res = client.post('/auth/logout')
    assert res.status_code == 401
    assert res.json().get('detail') == 'Not authenticated'

def test_auth_failure_missing_refresh_token(client, random_unmatched_tokens):
    access_token = random_unmatched_tokens[0]
    res = client.post(
        '/auth/logout',
        headers={'Authorization': 'Bearer ' + access_token}
    )
    assert res.status_code == 401
    assert res.json().get('detail') == 'Refresh token is missing'

def test_auth_failure_unmatched_tokens(client, random_unmatched_tokens):
    access_token, refresh_token = random_unmatched_tokens
    res = client.post(
        '/auth/logout',
        headers={'Authorization': 'Bearer ' + access_token},
        cookies={'refresh_token': refresh_token}
    )
    assert res.status_code == 400
    assert res.json().get('detail') == 'Access token and refresh token do not match'

