# 🏠 TTLock Airbnb Booking Integration 🏠

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)](https://www.python.org/downloads/release/python-390/)

Welcome to the **TTLock Airbnb Booking Integration** project! 🎉 This solution automates key management for Airbnb and Booking.com properties, making it ideal for HR and administrative teams in property management firms looking to enhance security, streamline processes, and provide a seamless experience for guests.

## ✨ Key Features

- 🔐 **Secure & Unique Access Codes**: Automatically generate time-sensitive access codes unique to each booking, minimizing security risks.
- ⏳ **Customizable Access Duration**: Codes are active only during the guest's stay, from check-in to check-out.
- 📬 **Automated Guest Communication**: Sends access details to guests via email or Airbnb messaging, reducing manual work.
- 🌍 **Multi-Platform Integration**: Works with both Airbnb and Booking.com to simplify access for multiple booking channels.
- 📈 **Efficient Workflow**: Automates key code generation and delivery, saving valuable administrative time.

## 🚀 Quick Start Guide

### 📋 Prerequisites

- **Python 3.9+**: Install from [Python's official site](https://www.python.org/downloads/)
- **TTLock Account**: [Register here](https://www.ttlock.com/)
- **API Access for Airbnb and Booking.com**: Contact Airbnb and Booking.com support to set up developer API access.

### 📦 Installation

1. **Clone this Repository**:

    ```bash
    git clone https://github.com/alexandrunite/TTLock-Airbnb-Booking-integration.git
    cd TTLock-Airbnb-Booking-integration
    ```

2. **Set Up a Virtual Environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the Required Libraries**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:

    Create a `.env` file with your credentials for secure access:

    ```plaintext
    TTLOCK_CLIENT_ID=your_ttlock_client_id
    TTLOCK_CLIENT_SECRET=your_ttlock_client_secret
    TTLOCK_USERNAME=your_ttlock_username
    TTLOCK_PASSWORD=your_ttlock_password
    AIRBNB_API_KEY=your_airbnb_api_key
    BOOKING_API_KEY=your_booking_api_key
    ```

    💡 *Note*: Keep your `.env` file private to ensure sensitive information stays secure.

### ⚙️ Configuration

- Open `config.py` to adjust settings like the duration for access codes, API endpoints, and notification methods.

## 🏃‍♂️ Running the Integration

1. **Start the Service**:

    ```bash
    python main.py
    ```

2. **Automated Notifications**: Once running, the integration will automatically send access codes for new bookings directly to the guests.

3. **Track Activity Logs**: View generated access codes and activity in `logs/access.log` for easy auditing.

## 🌐 Workflow Overview

1. **Real-Time Booking Monitoring**: The system constantly checks Airbnb and Booking.com for new reservations.
2. **Access Code Generation**: Unique pin codes are generated and assigned to each guest booking.
3. **Automated Messaging**: Codes are delivered to the guest via email or Airbnb messaging, ensuring clear communication.
4. **Automatic Expiration**: Codes expire after check-out, adding an additional layer of security.

## 🤝 Contributing

We welcome contributions to enhance this integration for more flexible use cases!

1. **Fork the Repo**: Click on the "Fork" button.
2. **Create a New Branch**: Make your updates in a new branch.
3. **Submit a Pull Request**: Describe the changes and submit.

## 🛡️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 🎖 Acknowledgments

- [TTLock API Documentation](https://open.ttlock.com/) – for detailed TTLock integration
- [Airbnb API Documentation](https://www.airbnb.com/api-documentation/) – for booking management
- [Booking API Documentation](https://developers.booking.com/) – for API integration

## 📞 Support

For questions, open an issue in this repository or reach out to our developer team!

---

Happy Hosting and Secure Access Management! 🏆
