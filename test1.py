import requests
from icalendar import Calendar, Event
from datetime import datetime
import threading
import time
import schedule

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
                
                # Filter: Only process events with 'Booking' in summary
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


def fetch_and_parse_feeds():
    # Replace with your actual iCal feed URLs
    airbnb_ical_url = ''
    # booking_ical_url = 'https://reservations.booking.com/ical/PROPERTY_ID.ics?s=XXXXXXXXXXXXXX'

    # Fetch iCal data
    airbnb_ical = fetch_ical(airbnb_ical_url)
    # booking_ical = fetch_ical(booking_ical_url)

    all_bookings = []

    # Parse Airbnb iCal data
    if airbnb_ical:
        airbnb_bookings = parse_ical(airbnb_ical)
        print(f"Found {len(airbnb_bookings)} bookings from Airbnb.")
        all_bookings.extend(airbnb_bookings)

    # Parse Booking.com iCal data
    # if booking_ical:
    #     booking_bookings = parse_ical(booking_ical)
    #     print(f"Found {len(booking_bookings)} bookings from Booking.com.")
    #     all_bookings.extend(booking_bookings)

    # Process bookings
    for booking in all_bookings:
        print(f"Booking Summary: {booking['summary']}")
        print(f"Start Date: {booking['start']}")
        print(f"End Date: {booking['end']}")
        print(f"UID: {booking['uid']}")
        print("---")
    
    # Here you can add code to generate PIN codes or perform other actions
    # For example:
    # for booking in all_bookings:
    #     generate_pin_code_for_booking(booking)

    return all_bookings

def run_scheduler():
    while True:
        print(f"Fetching and parsing iCal feeds at {datetime.now()}")
        fetch_and_parse_feeds()
        print("Waiting for 10 minutes...")
        time.sleep(600)  # Wait for 600 seconds (10 minutes)

if __name__ == "__main__":
    run_scheduler()
