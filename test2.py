import requests
import hashlib
import time
import random
import string
from datetime import datetime, timedelta
from icalendar import Calendar, Event
import pytz
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import json

# ----------------------------
# Configuration and Constants
# ----------------------------

# TT Lock Developer Credentials
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'

# TT Lock Account Credentials
USERNAME = 'your_email_or_phone_number'  # The one used in TT Lock App
PASSWORD = 'your_password'  # TT Lock App password

# Base URL for your region
BASE_URL = 'https://euapi.ttlock.com'  # Example for Europe

# Lock ID
LOCK_ID = 'your_lock_id'

# iCal Feed URLs
AIRBNB_ICAL_URL = 'https://www.airbnb.com/calendar/ical/1252013413294728027.ics?s=284ab85b91fca2ce7968d313ef7b2886'
# booking_ical_url = 'https://reservations.booking.com/ical/PROPERTY_ID.ics?s=XXXXXXXXXXXXXX'

# Path to store processed booking UIDs
PROCESSED_BOOKINGS_FILE = 'processed_bookings.json'

# SMTP Configuration for Email Sending
SMTP_SERVER = 'smtp.gmail.com'  # Example for Gmail
SMTP_PORT = 587
SMTP_USERNAME = 'your_email@gmail.com'
SMTP_PASSWORD = 'your_email_password'  # Consider using App Passwords

# PDF Template Path
PDF_TEMPLATE_PATH = 'instructions_template.pdf'  # Path to your PDF template

# ----------------------------
# Helper Functions
# ----------------------------

def load_processed_bookings():
    """Load the list of processed booking UIDs from a JSON file."""
    if not os.path.exists(PROCESSED_BOOKINGS_FILE):
        return set()
    try:
        with open(PROCESSED_BOOKINGS_FILE, 'r') as file:
            data = json.load(file)
            return set(data)
    except Exception as e:
        print(f"Error loading processed bookings: {e}")
        return set()

def save_processed_bookings(processed_uids):
    """Save the list of processed booking UIDs to a JSON file."""
    try:
        with open(PROCESSED_BOOKINGS_FILE, 'w') as file:
            json.dump(list(processed_uids), file)
    except Exception as e:
        print(f"Error saving processed bookings: {e}")

def generate_random_pin(length=6):
    """Generate a random PIN code of specified length."""
    # Ensure the first digit is not 0 to comply with some lock requirements
    first_digit = random.choice(string.digits[1:])
    other_digits = ''.join(random.choices(string.digits, k=length - 1))
    return first_digit + other_digits

# ----------------------------
# TTLock API Integration
# ----------------------------

def get_access_token():
    """Obtain an access token from the TTLock API."""
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

    try:
        response = requests.post(url, data=params, headers=headers, allow_redirects=False)
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)

        data = response.json()

        if 'access_token' in data:
            return data['access_token']
        else:
            errmsg = data.get('errmsg', 'Unknown error')
            raise Exception(f"Failed to obtain access token: {errmsg}")

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        raise Exception("Failed to parse access token response.")

def add_pin_code(access_token, lock_id, pin_code, start_date, end_date):
    """Add a permanent PIN code to the TTLock smart lock."""
    api_v3_url = f'{BASE_URL}/v3/keyboardPwd/add'
    timestamp = int(time.time() * 1000)

    params = {
        'clientId': CLIENT_ID,
        'accessToken': access_token,
        'lockId': lock_id,
        'keyboardPwd': pin_code,
        'keyboardPwdName': 'Booking PIN',  # Name for identification
        'startDate': int(start_date.timestamp() * 1000),
        'endDate': int(end_date.timestamp() * 1000),
        'addType': 2,  # 2 indicates a permanent PIN code
        'date': timestamp,
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(api_v3_url, data=params, headers=headers)
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)

        data = response.json()

        if 'errcode' in data:
            errmsg = data.get('errmsg', 'Unknown error')
            print(f"Failed to add PIN code: {errmsg}")
            raise Exception(f"Failed to add PIN code: {errmsg}")
        else:
            keyboardPwdId = data.get('keyboardPwdId')
            print(f"Successfully added PIN code {pin_code} to lock {lock_id}")
            print(f"Keyboard Password ID: {keyboardPwdId}")
            print(f"Response Data: {data}")
            return keyboardPwdId

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        raise Exception("Failed to parse PIN code addition response.")

# ----------------------------
# Email Sending Function
# ----------------------------

def send_email_with_pdf(recipient_email, subject, body, pdf_path):
    """Send an email with an attached PDF."""
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Attach the PDF
    try:
        with open(pdf_path, 'rb') as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(pdf_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
        msg.attach(part)
    except FileNotFoundError:
        print(f"PDF file not found at path: {pdf_path}")
        return

    try:
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")

# ----------------------------
# iCal Parsing and Inspection
# ----------------------------

def fetch_ical(url):
    """Fetch iCal data from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Successfully fetched iCal data from {url}")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching iCal data from {url}: {e}")
        return None

def parse_ical(ical_string):
    """Parse iCal data and extract booking events."""
    bookings = []
    try:
        cal = Calendar.from_ical(ical_string)
        for component in cal.walk():
            if component.name == "VEVENT":
                summary = str(component.get('summary', 'No Title'))
                
                # Filter: Only process events with 'Booking' or 'Reservation' in summary
                if 'Booking' not in summary and 'Reservation' not in summary:
                    print(f"Skipping non-booking event: {summary}")
                    continue  # Skip non-booking events
                
                dtstart_prop = component.get('dtstart')
                dtend_prop = component.get('dtend')
                uid = str(component.get('uid', 'No UID'))
                
                # Initialize start and end dates
                start_date = None
                end_date = None

                # Handle DTSTART
                if hasattr(dtstart_prop, 'dt'):
                    start_date = dtstart_prop.dt
                else:
                    # Attempt to parse as string if it's vText
                    start_str = dtstart_prop.to_ical().decode('utf-8')
                    try:
                        # Handle all-day events where date is provided without time
                        if 'T' not in start_str:
                            start_date = datetime.strptime(start_str, '%Y-%m-%d')
                        else:
                            start_date = datetime.fromisoformat(start_str)
                    except ValueError:
                        print(f"Unable to parse DTSTART: {start_str}")
                        continue  # Skip this event

                # Handle DTEND
                if hasattr(dtend_prop, 'dt'):
                    end_date = dtend_prop.dt
                else:
                    # Attempt to parse as string if it's vText
                    end_str = dtend_prop.to_ical().decode('utf-8')
                    try:
                        # Handle all-day events where date is provided without time
                        if 'T' not in end_str:
                            end_date = datetime.strptime(end_str, '%Y-%m-%d')
                        else:
                            end_date = datetime.fromisoformat(end_str)
                    except ValueError:
                        print(f"Unable to parse DTEND: {end_str}")
                        continue  # Skip this event

                # Placeholder for guest email extraction
                guest_email = extract_guest_email(uid)

                bookings.append({
                    'summary': summary,
                    'start': start_date,
                    'end': end_date,
                    'uid': uid,
                    'email': guest_email
                })
        return bookings
    except Exception as e:
        print(f"Error parsing iCal data: {e}")
        return []

def inspect_ical(ical_string):
    """Inspect and print all properties of each event in the iCal data."""
    try:
        cal = Calendar.from_ical(ical_string)
        for component in cal.walk():
            if component.name == "VEVENT":
                print("\n--- New Event ---")
                event = {}
                for key, value in component.items():
                    if hasattr(value, 'dt'):
                        dt = value.dt
                        if isinstance(dt, datetime):
                            event[key] = dt.isoformat()
                        else:
                            event[key] = str(dt)
                    else:
                        # For properties like SUMMARY, DESCRIPTION, etc.
                        event[key] = value.to_ical().decode('utf-8')
                pprint(event)
    except Exception as e:
        print(f"Error inspecting iCal data: {e}")

def extract_guest_email(uid):
    
    # Placeholder: Implement a lookup to retrieve the guest email based on UID
    # This could involve querying a database or using an external service
    # For demonstration, we'll return None
    return None

# ----------------------------
# Booking Processing
# ----------------------------

def process_new_bookings(bookings, processed_uids, access_token):
    """Process new bookings by generating and adding PIN codes, then sending instructions."""
    new_bookings = []

    for booking in bookings:
        uid = booking['uid']
        if uid not in processed_uids:
            new_bookings.append(booking)

    if not new_bookings:
        print("No new bookings to process.")
        return

    for booking in new_bookings:
        summary = booking['summary']
        start_date = booking['start']
        end_date = booking['end']
        uid = booking['uid']
        guest_email = booking.get('email')  # Ensure this is populated

        print(f"Processing new booking: {summary} from {start_date} to {end_date} (UID: {uid})")

        # Generate a permanent PIN code
        pin_code = generate_random_pin(length=6)

        try:
            # Add the PIN code to the lock
            keyboardPwdId = add_pin_code(access_token, LOCK_ID, pin_code, start_date, end_date)

            # Send PDF instructions to the guest
            if guest_email:
                subject = "Instrucțiuni pentru șederea la [Numele Proprietății]"
                body = f"Dragă oaspete,\n\nVă mulțumim pentru rezervarea efectuată pentru perioada {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}. Atașat găsiți un PDF cu instrucțiuni importante pentru șederea dumneavoastră.\n\nCu stimă,\n[Prenumele și Numele / Management Proprietate]"
                send_email_with_pdf(guest_email, subject, body, PDF_TEMPLATE_PATH)
            else:
                print(f"Nu s-a găsit un email pentru booking UID {uid}. Nu se trimite emailul.")

            # Adaugă UID-ul booking-ului la lista de procesate
            processed_uids.add(uid)

        except Exception as e:
            print(f"Error processing booking UID {uid}: {e}")

    # Salvează lista actualizată de booking-uri procesate
    save_processed_bookings(processed_uids)

# ----------------------------
# Main Function
# ----------------------------

def fetch_and_parse_feeds():
    """Fetch iCal feeds, parse bookings, and process new bookings."""
    print(f"\nFetching and parsing iCal feeds at {datetime.now()}\n")

    # Fetch Airbnb iCal data
    airbnb_ical = fetch_ical(AIRBNB_ICAL_URL)

    all_bookings = []

    # Parse Airbnb iCal data
    if airbnb_ical:
        airbnb_bookings = parse_ical(airbnb_ical)
        print(f"Found {len(airbnb_bookings)} bookings from Airbnb.")
        all_bookings.extend(airbnb_bookings)
    else:
        print("Failed to fetch Airbnb iCal data.")

    # Parse Booking.com iCal data
    # if booking_ical:
    #     booking_bookings = parse_ical(booking_ical)
    #     print(f"Found {len(booking_bookings)} bookings from Booking.com.")
    #     all_bookings.extend(booking_bookings)
    # else:
    #     print("Failed to fetch Booking.com iCal data.")

    # Procesarea booking-urilor
    if all_bookings:
        # Încarcă booking-urile procesate
        processed_uids = load_processed_bookings()

        # Obține access token-ul
        try:
            access_token = get_access_token()
        except Exception as e:
            print(f"Error obtaining access token: {e}")
            return

        # Procesează booking-urile noi
        process_new_bookings(all_bookings, processed_uids, access_token)
    else:
        print("No bookings found in iCal feeds.")

def run_scheduler():
    """Rulează funcția fetch_and_parse_feeds la fiecare 10 minute."""
    while True:
        fetch_and_parse_feeds()
        print("Waiting for 10 minutes...\n")
        time.sleep(600)  # Așteaptă 600 secunde (10 minute)

if __name__ == "__main__":
    run_scheduler()
