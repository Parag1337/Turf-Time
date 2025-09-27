# Turf Time Setup Instructions

## Environment Setup

1. **Create your .env file:**
   ```bash
   cp .env.template .env
   ```

2. **Configure your environment variables in .env:**
   - `SECRET_KEY`: Generate a secure random key for Flask sessions
   - `DB_USERNAME`: Your MySQL database username (default: turf_user)
   - `DB_PASSWORD`: Your MySQL database password  
   - `DB_HOST`: Database host (default: localhost)
   - `DB_NAME`: Database name (default: turf_time)
   - `MAIL_USERNAME`: Your email address for sending notifications
   - `MAIL_PASSWORD`: Your email app password (for Gmail, generate an app password)
   - `MAIL_DEFAULT_SENDER`: The "From" address for emails

## Database Setup

1. **Install MySQL/MariaDB** if not already installed
2. **Create the database:**
   ```sql
   CREATE DATABASE turf_time;
   CREATE USER 'turf_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON turf_time.* TO 'turf_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. **Initialize the database:**
   ```bash
   python init_db.py
   ```

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

## Email Configuration

For Gmail:
1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password for the application
3. Use the App Password (not your regular password) in `MAIL_PASSWORD`

## Troubleshooting

- If you get missing environment variable errors, ensure all required variables are set in your `.env` file
- If email sending fails, verify your email credentials and app password
- For database connection issues, check your MySQL server is running and credentials are correct

## Security Notes

- Never commit your `.env` file to version control
- Use strong, unique passwords for database and email accounts
- Generate a cryptographically secure SECRET_KEY for production