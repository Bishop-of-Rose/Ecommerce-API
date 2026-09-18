from src.schemas import UserResponse

def test_who_am_i(client, logged_in):
    access_token = logged_in[0]

    res = client.get('/users/whoami', headers={'Authorization': 'Bearer ' + access_token})
    assert res.status_code == 200
    user = UserResponse(**res.json())

def test_update_user(client, logged_in):
    access_token = logged_in[0]
    data = {
        'password': 'bishop'
    }

    res = client.put('/users', json=data, headers={'Authorization': 'Bearer ' + access_token})
    assert res.status_code == 200
    user = UserResponse(**res.json())

def test_delete_user(client, logged_in):
    access_token = logged_in[0]

    res = client.delete('/users', headers={'Authorization': 'Bearer ' + access_token})
    assert res.status_code == 204