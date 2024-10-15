import requests
from icalendar import Calendar, Event
from datetime import datetime
from pprint import pprint
import os

def fetch_ical(url):
    """
    Fetch iCal data from the given URL.
    """
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
                dtstart_prop = component.get('dtstart')
                dtend_prop = component.get('dtend')
                
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
                        end_date = datetime.fromisoformat(end_str)
                    except ValueError:
                        print(f"Unable to parse DTEND: {end_str}")
                        continue  # Skip this event

                uid = str(component.get('uid', 'No UID'))
                bookings.append({
                    'summary': summary,
                    'start': start_date,
                    'end': end_date,
                    'uid': uid
                })
        return bookings
    except Exception as e:
        print(f"Error parsing iCal data: {e}")
        return []

def inspect_events(cal):
    """
    Inspect and print details of each event in the Calendar.
    """
    for component in cal.walk():
        if component.name == "VEVENT":
            print("\n--- New Event ---")
            event = {}
            for key, value in component.items():
                # For datetime objects, convert to ISO format string
                if isinstance(value.dt, datetime):
                    event[key] = value.dt.isoformat()
                else:
                    event[key] = value.to_ical().decode('utf-8')
            pprint(event)

def main():
    # Replace with your actual iCal feed URL
    ical_url = 'https://www.airbnb.com/calendar/ical/1252013413294728027.ics?s=284ab85b91fca2ce7968d313ef7b2886'  # Example URL
    
    # Check if the URL has been set
    if 'example.com' in ical_url:
        print("Please replace 'https://www.example.com/calendar.ics' with your actual iCal feed URL.")
        return
    
    ical_data = fetch_ical(ical_url)
    if not ical_data:
        return
    
    cal = parse_ical(ical_data)
    if not cal:
        return
    
    inspect_events(cal)

if __name__ == '__main__':
    main()
