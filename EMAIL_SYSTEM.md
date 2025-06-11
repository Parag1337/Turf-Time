# Turf Time - Email System Documentation

## Email Configuration

The Turf Time application is configured to send emails for:
- Booking confirmations to users
- Booking notifications to turf owners
- Booking cancellations to users
- Booking cancellation notifications to turf owners

## Email Configuration Settings

Email settings are configured in `config.py`:

```python
# Email Configuration
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'turftime4@gmail.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'fggdasmdjpqezrwc')  # App password for Gmail with 2FA
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'Turf Time <turftime4@gmail.com>')
```

## Gmail Configuration

The system uses a Gmail account with the following credentials:
- Username: `turftime4@gmail.com`
- App Password: `fggdasmdjpqezrwc`

**Note:** This is an app-specific password generated for Gmail accounts with 2-factor authentication enabled. The app password bypasses 2FA but is specific to this application.

## Troubleshooting Email Issues

If you experience issues with email sending, you can use the following tools:

1. **Email System Fix Utility**: Run `python email_system_fix.py` to automatically diagnose and fix common email configuration issues.

2. **Checking Email Addresses**: Run `python check_email_addresses.py` to verify that all email addresses in the database are valid.

3. **Common Issues:**
   - Make sure the Gmail app password does not contain spaces
   - Ensure TLS is enabled for port 587
   - Check that Flask-Mail is properly installed 
   - Verify that the recipient email addresses are valid

## Maintaining the Email System

### Adding New Email Templates

Email templates are stored in the `templates/emails/` directory. To add a new email template:

1. Create a new HTML file in the `templates/emails/` directory
2. Design your email template using HTML
3. Add a function to `utils/email_utils.py` to send the new type of email

### Changing Email Account

If you need to change the email account used for sending:

1. Update the email settings in `config.py`
2. If using Gmail, generate a new app password from Google account settings
3. Run the `email_system_fix.py` script to verify the new configuration

## Available Email Templates

The following email templates are available:

- `booking_confirmation.html` - Sent to users when they make a booking
- `owner_booking_notification.html` - Sent to turf owners when a booking is made
- `booking_cancellation.html` - Sent to users when a booking is cancelled
- `owner_cancellation_notification.html` - Sent to turf owners when a booking is cancelled

## Email Sending Logic

Email sending logic is encapsulated in the `utils/email_utils.py` file. The main functions are:

- `send_booking_confirmation_email(booking)` - Sends booking confirmation to users
- `send_booking_notification_to_owner(booking)` - Sends booking notification to turf owners
- `send_cancellation_notification_to_user(booking)` - Sends cancellation notification to users
- `send_cancellation_notification_to_owner(booking)` - Sends cancellation notification to turf owners

Emails are sent asynchronously to avoid blocking the web server during email delivery.
