import requests
from icalendar import Calendar
from datetime import datetime
from database import add_guest_info

def fetch_ical(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching iCal data from {url}: {e}")
        return None

def parse_ical(ical_string):
    bookings = []
    try:
        cal = Calendar.from_ical(ical_string)
        for component in cal.walk():
            if component.name == "VEVENT":
                summary = str(component.get('summary', 'No Title'))
                if 'Booking' not in summary and 'Reservation' not in summary:
                    continue
                dtstart_prop = component.get('dtstart')
                dtend_prop = component.get('dtend')
                uid = str(component.get('uid', 'No UID'))
                start_date = None
                end_date = None
                if hasattr(dtstart_prop, 'dt'):
                    start_date = dtstart_prop.dt
                else:
                    start_str = dtstart_prop.to_ical().decode('utf-8')
                    try:
                        if 'T' not in start_str:
                            start_date = datetime.strptime(start_str, '%Y-%m-%d')
                        else:
                            start_date = datetime.fromisoformat(start_str)
                    except ValueError:
                        continue
                if hasattr(dtend_prop, 'dt'):
                    end_date = dtend_prop.dt
                else:
                    end_str = dtend_prop.to_ical().decode('utf-8')
                    try:
                        if 'T' not in end_str:
                            end_date = datetime.strptime(end_str, '%Y-%m-%d')
                        else:
                            end_date = datetime.fromisoformat(end_str)
                    except ValueError:
                        continue
                bookings.append({
                    'summary': summary,
                    'start': start_date,
                    'end': end_date,
                    'uid': uid
                })
    except Exception as e:
        print(f"Error parsing iCal data: {e}")
    return bookings
