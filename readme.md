Here's a polished and engaging `README.md` file for your project:

---

# 🏠 Airbnb/Booking.com TTLock Integration System 🛡️

> **An all-in-one solution for managing Airbnb and Booking.com reservations with automated smart lock PIN code generation, guest communication, and invoicing.**

## 🌟 Overview

This project is a Python-based application designed to streamline short-term rental management by integrating with TTLock smart locks. With automatic booking sync, PIN code generation, and invoicing capabilities, this system simplifies check-ins and enhances security. A user-friendly GUI built with Tkinter provides easy control over the entire process.

## 🎯 Key Features

- **🔒 Automated PIN Generation**: Generates unique PIN codes for each booking, ensuring secure guest access via TTLock API.
- **📅 Booking Sync**: Regularly syncs with Airbnb and Booking.com calendars to fetch and process new bookings.
- **📧 Email Integration**: Parses booking confirmation emails, extracts guest details, and sends personalized confirmation emails with PIN codes and instructions.
- **📄 Invoice Generation**: Creates and attaches invoices for each stay based on booking details.
- **🖥️ Intuitive GUI**: User-friendly control panel with options for manual sync, email checking, viewing bookings, logs, and scheduler control.
- **📊 Logging & Monitoring**: Centralized logging to monitor activity and catch any issues.

## 🖼️ Screenshots

### Main Dashboard
![Dashboard](https://user-images.githubusercontent.com/yourusername/dashboard-screenshot.png)

### Bookings View
![Bookings View](https://user-images.githubusercontent.com/yourusername/bookings-view.png)

## 🛠️ Tech Stack

- **Python**: Core application logic
- **Tkinter**: GUI for user-friendly control
- **SQLite**: Database to store booking information
- **TTLock API**: Smart lock PIN management
- **iCal**: Parsing bookings from Airbnb/Booking.com
- **SMTP (Gmail)**: Email sending and receiving

## 🚀 Quick Start

### Prerequisites

- **Python 3.x**
- **Virtual Environment (Optional but recommended)**
- Airbnb and Booking.com iCal URLs
- TTLock API credentials
- Gmail account for sending emails

### Installation

1. **Clone the Repository**

   
   git clone https://github.com/yourusername/airbnb-ttlock-integration.git
   cd airbnb-ttlock-integration
   

2. **Set Up Environment Variables**

   Create a `.env` file in the root directory with the following content:

   
   CLIENT_ID=your_client_id
   CLIENT_SECRET=your_client_secret
   USERNAME=your_username
   PASSWORD=your_password
   BASE_URL=https://euapi.ttlock.com
   LOCK_ID=your_lock_id
   AIRBNB_ICAL_URL=https://www.airbnb.com/calendar/ical/your_ical_url.ics
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=your_email_password
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   PDF_TEMPLATE_PATH=templates/invoice_template.pdf
   TUTORIAL_LINK=https://yourwebsite.com/tutorial
   PRICE_PER_NIGHT=100.0
   LOGGING_LEVEL=INFO
   LOGGING_FILE=ttlock_integration.log
   DATABASE_FILE=bookings.db
   

3. **Install Dependencies**

   
   pip install -r requirements.txt
   

4. **Run the Application**

   
   python main.py
   

## 🎛️ Features Breakdown

### Sync Bookings
- Fetches and processes bookings from Airbnb/Booking.com iCal feeds.
- Generates unique PIN codes for each booking and stores them in the TTLock system.

### Check Emails
- Parses new emails for guest details, such as name and email, which are then saved for future correspondence.
- Uses Gmail SMTP for sending booking confirmation emails with invoice and PIN code.

### View Bookings
- Displays all processed bookings, including check-in/check-out dates, PIN code, and invoice path.

### View Logs
- Displays real-time application logs for easy monitoring and troubleshooting.

### Scheduler
- Runs booking sync and email check tasks every 10 minutes, ensuring the system is always up-to-date.


## 📝 To-Do List

- [ ] Add SMS notifications for guests (via Twilio).
- [ ] Enhance error handling with retry logic.
- [ ] Add multi-language support for guests’ emails.

## 📚 Documentation

### Configuration

All environment-specific configurations are managed through a `.env` file. Ensure you populate it correctly as shown in the installation steps above.

### Logging

Logs are saved to a specified file (`ttlock_integration.log`) for real-time monitoring. You can view these logs directly within the GUI under the "View Logs" tab.

## 🤝 Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss improvements.

## 📄 License

This project is licensed under the MIT License.

## 🌐 Connect with Me

- **GitHub**: [@yourusername](https://github.com/alexandrunite)
- **LinkedIn**: [Your LinkedIn Profile](https://www.linkedin.com/in/alexandru-nite/)

**Thank you for visiting my project! 😊 Let me know if you have any questions or feedback.**
