import requests
import hashlib
import time
from config import CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, BASE_URL, LOCK_ID

def get_access_token():
    url = f'{BASE_URL}/oauth2/token'
    timestamp = int(time.time() * 1000)
    password_md5 = hashlib.md5(PASSWORD.encode('utf-8')).hexdigest()
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'username': USERNAME,
        'password': password_md5,
        'grant_type': 'password',
        'redirect_uri': 'https://open.ttlock.com',
        'timestamp': timestamp,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(url, data=params, headers=headers, allow_redirects=False)
    data = response.json()
    if 'access_token' in data:
        return data['access_token']
    else:
        errmsg = data.get('errmsg', 'Unknown error')
        raise Exception(f"Failed to obtain access token: {errmsg}")

def add_pin_code(access_token, lock_id, pin_code, start_date, end_date):
    api_v3_url = f'{BASE_URL}/v3/keyboardPwd/add'
    timestamp = int(time.time() * 1000)
    params = {
        'clientId': CLIENT_ID,
        'accessToken': access_token,
        'lockId': lock_id,
        'keyboardPwd': pin_code,
        'keyboardPwdName': 'Booking PIN',
        'startDate': int(start_date.timestamp() * 1000),
        'endDate': int(end_date.timestamp() * 1000),
        'addType': 2,
        'date': timestamp,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(api_v3_url, data=params, headers=headers)
    data = response.json()
    if 'errcode' in data:
        errmsg = data.get('errmsg', 'Unknown error')
        raise Exception(f"Failed to add PIN code: {errmsg}")
    else:
        keyboardPwdId = data.get('keyboardPwdId')
        return keyboardPwdId
