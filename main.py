import requests
import hashlib
import time
import random
import string
from datetime import datetime, timedelta
from icalendar import Calendar, Event
import pytz
import os


def fetch_ical(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"am tras cu succes datele din iCal")
        return reponse.text
    expect:
        print(f"Error fetching the data")
        return None

def parse_ical(ical_string):
    try:
        cal = Calendar.from_ical(ical_string)
        print("parsed")
        return cal
    except Exception as e:
        print("eroare la parsare: {e}")
        return None

def inspect_events(cal):
    

# TT Lock Developer Credentials (Replace with your actual credentials)
CLIENT_ID = ''
CLIENT_SECRET = ''

# TT Lock Account Credentials (Replace with your actual credentials)
USERNAME = ''  # The one used in TT Lock App
PASSWORD = ''  # TT Lock App password

# Base URL for your region (Update as needed)
BASE_URL = ''

# Lock ID (Replace with your actual lock ID)
LOCK_ID = ''

def get_access_token():
    # Correct OAuth2 token endpoint (without /v3)
    url = f'{BASE_URL}/oauth2/token'
    timestamp = int(time.time() * 1000)

    # Encrypt the password using MD5
    password_md5 = hashlib.md5(PASSWORD.encode('utf-8')).hexdigest()

    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'username': USERNAME,
        'password': password_md5,
        'grant_type': 'password',
        'redirect_uri': 'https://open.ttlock.com',  # Ensure this matches your registered redirect URI
        'timestamp': timestamp,
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Use POST request instead of GET
    response = requests.post(url, data=params, headers=headers, allow_redirects=False)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        data = response.json()
    except Exception as e:
        print("JSON Decode Error:", e)
        data = None

    if data and 'access_token' in data:
        return data['access_token']
    else:
        raise Exception(f"Failed to obtain access token: {data}")

def generate_random_pin(length=6):
    return ''.join(random.choices(string.digits, k=length))

def add_pin_code(access_token, lock_id, pin_code, start_date, end_date):
    api_v3_url = f'{BASE_URL}/v3/keyboardPwd/add'
    timestamp = int(time.time() * 1000)

    params = {
        'clientId': CLIENT_ID,
        'accessToken': access_token,
        'lockId': lock_id,
        'keyboardPwd': pin_code,
        'keywordPwdName': 'test alex cod',
        'startDate': int(start_date.timestamp() * 1000),
        'endDate': int(end_date.timestamp() * 1000),
        'addType': 2,  # 1 indicates a time-limited PIN
        'date': timestamp,
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(api_v3_url, data=params, headers=headers)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        data = response.json()
    except Exception as e:
        print("JSON Decode Error:", e)
        print("Failed to parse response as JSON. The response might not be in JSON format.")
        data = None
        raise Exception(f"Failed to add PIN code due to response parsing error.")

    if data is None:
        raise Exception("Failed to parse response as JSON.")

    if 'errcode' in data:
        print(f"Failed to add PIN code: {data}")
        raise Exception(f"Failed to add PIN code: {data}")
    else:
        print(f"Successfully added PIN code {pin_code} to lock {lock_id}")
        print(f"Response Data: {data}")

def main():
    access_token = get_access_token()

    pin_code = generate_random_pin(length=6)

    start_date = datetime.now()
    end_date = start_date + timedelta(days=1)

    # add_pin_code(access_token, LOCK_ID, pin_code, start_date, end_date)

    print(f"Generated PIN Code: {pin_code}")
    print(f"Valid From: {start_date}")
    print(f"Valid Until: {end_date}")

if __name__ == '__main__':
    main()
