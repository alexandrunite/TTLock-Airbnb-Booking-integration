import imaplib
import email
from email.header import decode_header
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from config import SMTP_USERNAME, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT, TUTORIAL_LINK
from database import add_guest_info, get_booking
import re
import os

def check_new_emails():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.select("inbox")
    status, messages = mail.search(None, '(UNSEEN SUBJECT "Booking Confirmation")')
    email_ids = messages[0].split()
    for email_id in email_ids:
        res, msg = mail.fetch(email_id, "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()
                guest_email = extract_email_from_body(body)
                guest_name = extract_name_from_body(body)
                booking_uid = extract_uid_from_body(body)
                if booking_uid:
                    booking = get_booking(booking_uid)
                    if booking:
                        add_guest_info(booking_uid, guest_email, None)
                        send_confirmation_email(guest_email, guest_name, booking_uid, booking['pin_code'])
        mark_as_read(mail, email_id)
    mail.logout()

def extract_email_from_body(body):
    match = re.search(r'Email:\s*([\w\.-]+@[\w\.-]+)', body)
    if match:
        return match.group(1)
    return None

def extract_name_from_body(body):
    match = re.search(r'Name:\s*(.+)', body)
    if match:
        return match.group(1).strip()
    return None

def extract_uid_from_body(body):
    match = re.search(r'UID:\s*([\w\-]+)', body)
    if match:
        return match.group(1)
    return None

def mark_as_read(mail, msg_id):
    mail.store(msg_id, '+FLAGS', '\\Seen')

def send_confirmation_email(recipient_email, guest_name, booking_uid, pin_code):
    subject = "Instrucțiuni și Factură pentru Șederea Dumneavoastră la [Numele Proprietății]"
    body = f"Dragă {guest_name},\n\nVă mulțumim pentru rezervarea efectuată pentru UID {booking_uid}. Atașat găsiți factura și codul PIN pentru acces.\n\nCod PIN: {pin_code}\n\nPentru instrucțiuni suplimentare, vizitați {TUTORIAL_LINK}.\n\nCu stimă,\n[Prenumele și Numele / Management Proprietate]"
    send_email(recipient_email, subject, body, attachment_path=None)

def send_email(recipient_email, subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(part)
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")
