import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
BASE_URL = os.getenv('BASE_URL')
LOCK_ID = os.getenv('LOCK_ID')
AIRBNB_ICAL_URL = os.getenv('AIRBNB_ICAL_URL')
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
PDF_TEMPLATE_PATH = os.getenv('PDF_TEMPLATE_PATH', 'templates/invoice_template.pdf')
TUTORIAL_LINK = os.getenv('TUTORIAL_LINK', 'https://yourwebsite.com/tutorial')
