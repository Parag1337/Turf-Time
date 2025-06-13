

# TurfTime 🏟️  
**A Comprehensive Turf Booking and Management Platform**

TurfTime is a powerful web application designed to bridge the gap between turf owners and sports enthusiasts. It enables users to book turfs, find teammates, and manage team play — all while offering turf owners an intuitive dashboard to manage listings, revenue, and scheduling.

---

## 🚀 Features

### 👥 User Roles

#### ✅ Regular Users
- Browse and book available turfs
- Create public or private bookings
- Manage team participation
- View booking history and calendar
- Maintain personal profiles

#### 🧑‍💼 Turf Owners
- Manage turf listings (CRUD)
- Set pricing and availability
- View booking calendar and revenue statistics
- Manage incoming bookings

---

## 🏗️ System Architecture

| Layer | Technology |
|-------|------------|
| Backend | Flask (Python) |
| Database | MySQL + SQLAlchemy |
| ORM | SQLAlchemy |
| Authentication | Flask-Login |
| Forms & Validation | Flask-WTF |
| Email | Flask-Mail (Gmail SMTP) |
| Frontend | HTML, CSS, Bootstrap, JS |
| Charts | Chart.js or similar |
| Utilities | Environment Config, Email Utils |

---

## 📁 Project Structure

```

Turf-Time/  
├── app.py # App entry point  
├── config.py # App configuration  
├── forms.py # Form definitions  
├── init_db.py # Initializes DB  
├── fix_db.py # Schema update script  
├── database/  
│ ├── **init**.py  
│ ├── db_setup.py  
│ └── models.py  
├── routes/  
│ ├── **init**.py  
│ ├── auth.py # Auth routes  
│ ├── owner.py # Owner routes  
│ └── user.py # User routes  
├── static/  
│ ├── css/  
│ ├── img/  
│ ├── js/  
│ └── uploads/ # User-uploaded images  
├── templates/  
│ ├── auth/  
│ ├── emails/ # HTML Email templates  
│ ├── user/  
│ └── owner/  
├── utils/  
│ ├── **init**.py  
│ └── email_utils.py # Email sender  
└── .env # Environment vars (not tracked)

```

---

## 🧑‍💻 Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Turf-Time
```

2. **Create and activate virtual environment**
    
    ```bash
    python -m venv venv
    source venv/bin/activate     # On Windows: venv\Scripts\activate
    ```
    
3. **Install dependencies**
    
    ```bash
    pip install -r requirements.txt
    ```
    
4. **Configure Environment**
    
    ```bash
    cp .env.example .env
    # Then edit .env to add your DB and Gmail SMTP credentials
    ```
    
5. **Initialize the database**
    
    ```bash
    python init_db.py
    ```
    
6. **Update schema for team requests**
    
    ```bash
    python fix_db.py
    ```
    

---

## 🛠️ Core Functionalities

### 🌱 Booking Management

- Real-time availability
    
- Booking calendar integration
    
- Cancelation and status tracking
    
- Public booking for teammate discovery
    

### 🤝 Team Finding System

- Public bookings with notes and max players
    
- Join request system with status tracking
    
- Email notifications for invites and approvals
    

### 📬 Email Notifications

- Booking confirmation/cancellation
    
- Team join requests and approvals
    
- Turf booking alerts for owners
    

**Tech:** Flask-Mail with Gmail SMTP (App Password Required)

---

## 🧑‍🔒 Authentication & Security

- User registration with email verification
    
- Login with remember-me option
    
- Role-based access control (User / Owner)
    
- CSRF protection
    
- Password hashing (Werkzeug)
    
- Environment variables for sensitive data
    

---

## 📊 Dashboards & Visualizations

- Booking statistics (user/owner)
    
- Revenue charts for owners
    
- Calendar views for bookings
    
- Status color indicators (Pending, Confirmed, Canceled)
    

---

## 💻 Frontend & UX Highlights

- Responsive layout (Bootstrap 5)
    
- Interactive modals and calendar pickers
    
- Hover animations and ripple effects
    
- Toast alerts and confirmation dialogs
    
- Clean card-based UI system
---

## 🧪 Maintenance & Dev Tools

|Script|Purpose|
|---|---|
|`init_db.py`|Initial database creation|
|`fix_db.py`|Schema update for team functionality|
|`update_schema.py`|Optional DB schema updates|
|`email_utils.py`|Email diagnostic tools|

    

---

## 🔐 Known Issues & Fixes

|Issue|Solution|
|---|---|
|Gmail SMTP blocked|Use App Password with 2FA|
|DB schema mismatch|Run `fix_db.py` or `update_schema.py`|
|Email delivery delay|Check spam or SMTP logs|

---

## 👏 Contributing

Pull requests are welcome!  
For major changes, please open an issue first to discuss what you’d like to change.

---

## 📜 License

This project is licensed under the MIT License.

---


