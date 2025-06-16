# TurfTime 🏟️

**A Comprehensive Turf Booking and Management Platform**

TurfTime is a powerful full-stack web application that connects sports enthusiasts with turf facility owners. It simplifies the booking process, enables team formation, and provides advanced business analytics for owners. This project demonstrates robust backend logic, secure authentication, real-time scheduling, and intuitive frontend design.

---

## 🚀 Features

### 👥 User Roles

#### ✅ Regular Users

- Search and browse available turfs
    
- Create private or public bookings
    
- Join public team bookings via approval
    
- Track booking history and manage calendar
    
- Maintain and update personal profile
    

#### 🧑‍🎼 Turf Owners

- Register and manage multiple turf listings
    
- Set pricing, availability, and amenities
    
- View booking calendar and incoming reservations
    
- Analyze revenue statistics with custom date filters
    

---

## 🏗️ Technology Stack

|Layer|Tools & Technologies|
|---|---|
|Backend|Flask (Python), Flask-Login, Flask-WTF, Flask-Mail, Flask-SQLAlchemy|
|Frontend|HTML5, CSS3, Bootstrap 5, JavaScript (ES6+), Chart.js|
|Database|MySQL with SQLAlchemy ORM|
|Email System|Gmail SMTP via Flask-Mail|
|Security|CSRF protection, password hashing, role-based access control|
|Configuration|Python-dotenv (.env), modular Flask app factory pattern|

---

## 📁 Project Structure

```bash
Turf-Time/  
├── app.py                 # App entry point (Flask Factory)
├── config.py              # Config class for environments
├── requirements.txt       # Python dependencies
├── init_db.py             # Database initialization script
├── fix_db.py              # Script to update schema for team functionality
├── update_schema.py       # Additional schema updates
├── routes/                # Route Blueprints
│   ├── auth.py            # Authentication routes
│   ├── user.py            # User-facing functionality
│   └── owner.py           # Turf Owner functionalities
├── database/              # DB setup and models
│   ├── db_setup.py        # Connection and session configs
│   └── models.py          # SQLAlchemy ORM models
├── templates/             # Jinja2 HTML Templates
│   ├── auth/              # Auth pages
│   ├── user/              # User dashboard, bookings
│   └── owner/             # Turf management pages
├── static/                # Static files
│   ├── css/
│   ├── js/
│   ├── img/
│   └── uploads/           # Turf images and user content
├── utils/                 # Utilities (email, validators)
│   └── email_utils.py
└── .env                   # Local environment variables (excluded in .gitignore)
```

---

## 🧑‍💻 Installation & Setup

This guide walks you through the complete setup to run the TurfTime application locally in a development environment.

---

### ⚙️ Prerequisites

Ensure the following software is installed on your machine:

- **Python** ≥ 3.7
- **MySQL Server**

---

### 🛠️ Step-by-Step Setup

#### 📥 Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/turf-time.git
cd Turf-Time

```
#### 🧪 Step 2: Create and Activate a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 📦 Step 3: Install Project Dependencies

```bash
pip install -r requirements.txt
```

This installs all Flask-related packages and other dependencies defined in `requirements.txt`.

---

#### 🔐 Step 4: Configure Environment Variables

1. Create a `.env` file in the root directory:
    
    ```bash
    cp .env.example .env
    ```
    
2. Edit `.env` and set your own values:
    
    ```env
    DB_USERNAME=your_mysql_username
    DB_PASSWORD=your_mysql_password
    DB_NAME=turfdb
    
    SECRET_KEY=your_flask_secret_key
    
    MAIL_USERNAME=your_gmail@gmail.com
    MAIL_PASSWORD=your_gmail_app_password
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=587
    MAIL_USE_TLS=True
    ```
    

✅ Ensure `.env` is **NOT committed to GitHub** (already listed in `.gitignore`).

---

#### 🏗️ Step 5: Initialize the MySQL Database

1. Login to MySQL and create the DB:
    

```bash
mysql -u root -p
```

Inside MySQL shell:

```sql
CREATE DATABASE turfdb;
EXIT;
```

2. Run the DB initialization script:
    

```bash
python init_db.py
```

---

#### 🚀 Step 6: Start the Development Server

You can now launch the application locally:

```bash
flask run --debug
```

Or using the main app file:

```bash
python app.py
```

The app should now be accessible at:  
👉 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

### 🧪 Accessing Different User Roles

- **Regular User:** Register at `/register`
    
- **Turf Owner:** Register at `/register/owner`
    

Explore the dashboard functionality for both roles for testing.

---

### 🛠️ Troubleshooting

#### 🐬 Database Connection Issues

- Check `.env` for correct MySQL credentials
    
- Ensure MySQL service is running
    
- If schema issues persist, try:
    
    ```bash
    python fix_db.py
    ```
    

#### 📧 Email Not Sending

- Use a [Gmail App Password](https://myaccount.google.com/apppasswords)
    
- Enable **Less Secure App Access** (if needed)
    
- Double-check credentials in `.env`
    

#### 🧩 Missing Dependencies

If a package is missing or outdated:

```bash
pip install -r requirements.txt --upgrade
```

---
## 🌱 Core Functionalities

### 🗓️ Booking Management

- Real-time availability checking
    
- Booking creation (public/private)
    
- Status tracking (Pending / Confirmed / Cancelled)
    
- Interactive calendar integration
    
- Conflict detection algorithm to prevent double-booking
    

### 🤝 Team Formation

- Create or join public bookings
    
- Team size and player limits
    
- Approval system for join requests
    
- Email notifications on actions (invites, acceptance)
    

### 📨 Email System

- Confirmation and cancellation notifications
    
- Invitations and updates to users
    
- Admin alerts for turf bookings
    

### 📊 Dashboards & Analytics

- Booking stats per day/week/month
    
- Revenue charts (Bar, Pie)
    
- Booking heatmaps (Planned)
    
- Calendar view with status color codes
    

---

## 🔐 Security Measures

- CSRF protection via Flask-WTF
    
- Password hashing using Werkzeug (bcrypt)
    
- Email verification with time-limited tokens
    
- Role-based access control
    
- Environment variables for sensitive configuration
    
- Input validation and sanitization using WTForms
    

---

## 🧑‍🎨 Frontend Features

- Responsive Bootstrap 5 layout
    
- Intuitive modals and toast messages
    
- Dynamic forms with custom JavaScript validation
    
- Status badges and colored alerts
    
- Dashboard animations and hover effects
    

---

## 🛠️ Developer Utilities

|Script|Purpose|
|---|---|
|`init_db.py`|Initializes the database|
|`fix_db.py`|Adds team request schema fields|
|`update_schema.py`|Performs optional DB schema updates|
|`email_utils.py`|Utility for testing email functionality|

---

## ⚠️ Known Issues & Fixes

|Issue|Resolution|
|---|---|
|Gmail SMTP fails|Use App Password (Google Account > Security)|
|Schema mismatch|Run `fix_db.py` again|
|Email delivery slow|Check spam folder or SMTP rate limits|

---

## 🤝 Contributing

We welcome contributions from the community. To contribute:

1. Fork the repository
    
2. Create your feature branch (`git checkout -b feature-name`)
    
3. Commit your changes (`git commit -am 'Add new feature'`)
    
4. Push to the branch (`git push origin feature-name`)
    
5. Create a new Pull Request
    

Please open an issue first to discuss any major changes you’d like to propose.

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## 🔒 Environment Configuration

Copy the `.env.example` file:

```bash
cp .env.example .env
```

Then fill in your configuration:

```env
# MySQL Configuration
DB_USERNAME=root
DB_PASSWORD=yourpassword
DB_NAME=turf_db

# Secret key for sessions
SECRET_KEY=your_flask_secret_key

# Gmail SMTP for sending emails
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
```


---

## 📈 Future Roadmap

-  Payment gateway integration (Razorpay / Stripe)
    
-  Mobile-first API endpoints (REST/GraphQL)
    
-  Admin dashboard for site-wide analytics
    
-  Occupancy prediction using ML models
    
-  Loyalty system and referral tracking
    
-  Turf discovery map with live availability
    

---


## 🙌 Acknowledgements

- Flask documentation and community
- Bootstrap 5 open-source components
- Chart.js for stunning analytics
- WTForms & Flask-WTF for secure form handling
- Community contributors and testers
- [Font Awesome](https://fontawesome.com/) for icons
- [MySQL Community Edition](https://www.mysql.com/products/community/)

---

