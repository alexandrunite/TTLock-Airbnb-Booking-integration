import threading
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from ttlock_api import get_access_token, add_pin_code
from ical_parser import fetch_ical, parse_ical
from email_handler import check_new_emails, send_email
from pdf_generator import generate_invoice
from database import initialize_db, is_booking_processed, mark_booking_as_processed, add_guest_info, get_guest_info, get_all_bookings
from config import AIRBNB_ICAL_URL, LOCK_ID, PDF_TEMPLATE_PATH, TUTORIAL_LINK, PRICE_PER_NIGHT, LOGGING_FILE
from logging_setup import setup_logging
import logging
import os

def generate_random_pin(length=6):
    import random
    import string
    first_digit = random.choice(string.digits[1:])
    other_digits = ''.join(random.choices(string.digits, k=length - 1))
    return first_digit + other_digits

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TTLock Integration Control Panel")
        self.geometry("800x600")
        self.create_widgets()
        self.scheduler_running = False
        self.scheduler_thread = None

    def create_widgets(self):
        tab_control = ttk.Notebook(self)
        
        self.tab_control = tab_control

        self.sync_tab = ttk.Frame(tab_control)
        self.email_tab = ttk.Frame(tab_control)
        self.view_tab = ttk.Frame(tab_control)
        self.log_tab = ttk.Frame(tab_control)
        self.scheduler_tab = ttk.Frame(tab_control)

        tab_control.add(self.sync_tab, text='Sync Bookings')
        tab_control.add(self.email_tab, text='Check Emails')
        tab_control.add(self.view_tab, text='View Bookings')
        tab_control.add(self.log_tab, text='View Logs')
        tab_control.add(self.scheduler_tab, text='Scheduler')

        tab_control.pack(expand=1, fill='both')

        # Sync Tab
        sync_button = ttk.Button(self.sync_tab, text="Sync Now", command=self.sync_bookings)
        sync_button.pack(pady=20)

        self.sync_status = tk.StringVar()
        self.sync_status.set("Status: Idle")
        sync_status_label = ttk.Label(self.sync_tab, textvariable=self.sync_status)
        sync_status_label.pack()

        # Email Tab
        email_button = ttk.Button(self.email_tab, text="Check Emails", command=self.check_emails)
        email_button.pack(pady=20)

        self.email_status = tk.StringVar()
        self.email_status.set("Status: Idle")
        email_status_label = ttk.Label(self.email_tab, textvariable=self.email_status)
        email_status_label.pack()

        # View Bookings Tab
        view_button = ttk.Button(self.view_tab, text="Refresh Bookings", command=self.view_bookings)
        view_button.pack(pady=10)

        self.bookings_tree = ttk.Treeview(self.view_tab, columns=('UID', 'Summary', 'Check-In', 'Check-Out', 'PIN Code', 'Invoice Path', 'Date Processed'), show='headings')
        for col in self.bookings_tree['columns']:
            self.bookings_tree.heading(col, text=col)
            self.bookings_tree.column(col, width=100)
        self.bookings_tree.pack(expand=True, fill='both')

        # View Logs Tab
        view_logs_button = ttk.Button(self.log_tab, text="Refresh Logs", command=self.view_logs)
        view_logs_button.pack(pady=10)

        self.log_text = scrolledtext.ScrolledText(self.log_tab, wrap=tk.WORD)
        self.log_text.pack(expand=True, fill='both')

        # Scheduler Tab
        start_button = ttk.Button(self.scheduler_tab, text="Start Scheduler", command=self.start_scheduler)
        start_button.pack(pady=10)

        stop_button = ttk.Button(self.scheduler_tab, text="Stop Scheduler", command=self.stop_scheduler)
        stop_button.pack(pady=10)

        self.scheduler_status = tk.StringVar()
        self.scheduler_status.set("Scheduler Status: Stopped")
        scheduler_status_label = ttk.Label(self.scheduler_tab, textvariable=self.scheduler_status)
        scheduler_status_label.pack()

    def sync_bookings(self):
        def task():
            try:
                self.sync_status.set("Status: Syncing...")
                access_token = get_access_token()
                ical_data = fetch_ical(AIRBNB_ICAL_URL)
                if not ical_data:
                    self.sync_status.set("Status: Failed to fetch iCal data.")
                    return
                bookings = parse_ical(ical_data)
                for booking in bookings:
                    uid = booking['uid']
                    if is_booking_processed(uid):
                        continue
                    summary = booking['summary']
                    check_in = booking['start']
                    check_out = booking['end']
                    pin_code = generate_random_pin(length=6)
                    try:
                        keyboardPwdId = add_pin_code(access_token, LOCK_ID, pin_code, check_in, check_out)
                        add_guest_info(uid, None, None)
                        mark_booking_as_processed(uid)
                        logging.info(f"Added PIN code {pin_code} for booking UID {uid}.")
                    except Exception as e:
                        logging.error(f"Error adding PIN code for booking UID {uid}: {e}")
                self.sync_status.set("Status: Sync Completed.")
            except Exception as e:
                logging.error(f"Sync Error: {e}")
                self.sync_status.set("Status: Sync Failed.")

        threading.Thread(target=task).start()

    def check_emails(self):
        def task():
            try:
                self.email_status.set("Status: Checking Emails...")
                check_new_emails()
                self.email_status.set("Status: Email Check Completed.")
            except Exception as e:
                logging.error(f"Email Check Error: {e}")
                self.email_status.set("Status: Email Check Failed.")

        threading.Thread(target=task).start()

    def view_bookings(self):
        for item in self.bookings_tree.get_children():
            self.bookings_tree.delete(item)
        bookings = get_all_bookings()
        for booking in bookings:
            self.bookings_tree.insert('', 'end', values=(
                booking['uid'],
                booking['summary'],
                booking['check_in'],
                booking['check_out'],
                booking['pin_code'],
                booking['invoice_path'],
                booking['date_processed']
            ))

    def view_logs(self):
        if os.path.exists(LOGGING_FILE):
            with open(LOGGING_FILE, 'r') as f:
                logs = f.read()
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(tk.END, logs)
        else:
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, "Log file not found.")

    def start_scheduler(self):
        if not self.scheduler_running:
            self.scheduler_running = True
            self.scheduler_thread = threading.Thread(target=self.scheduler_task, daemon=True)
            self.scheduler_thread.start()
            self.scheduler_status.set("Scheduler Status: Running")
            logging.info("Scheduler started.")

    def stop_scheduler(self):
        if self.scheduler_running:
            self.scheduler_running = False
            self.scheduler_status.set("Scheduler Status: Stopped")
            logging.info("Scheduler stopped.")

    def scheduler_task(self):
        while self.scheduler_running:
            self.sync_bookings()
            self.check_emails()
            time.sleep(600)  # Wait for 10 minutes

def main():
    setup_logging()
    logging.info("Application started.")
    initialize_db()
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()
