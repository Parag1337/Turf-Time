from flask import render_template, current_app
from flask_mail import Message
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Use the mail instance from app.py
from app import mail

def send_email(subject, recipients, template, **kwargs):
    """Send an email using a template"""
    import traceback
    
    # Basic validation of recipients
    if not recipients or not all(recipients):
        print("ERROR: No valid recipients provided")
        return False
    
    try:
        app = current_app._get_current_object()
        
        print(f"📧 Sending email to {recipients}")
        print(f"📧 Subject: {subject}")
        
        # Create message with Flask-Mail
        msg = Message(
            subject=subject,
            recipients=recipients,
            sender=app.config['MAIL_DEFAULT_SENDER']
        )
        msg.html = render_template(template, **kwargs)
        
        # Try using Flask-Mail first
        try:
            print(f"📧 Using Flask-Mail with server: {app.config['MAIL_SERVER']}:{app.config['MAIL_PORT']}")
            
            # Optional debug logging of mail configuration
            print(f"📧 SSL Enabled: {app.config.get('MAIL_USE_SSL', False)}")
            print(f"📧 TLS Enabled: {app.config.get('MAIL_USE_TLS', False)}")
            print(f"📧 Sending as: {app.config['MAIL_DEFAULT_SENDER']}")
            
            # Send email
            mail.send(msg)
            print(f"✅ Email successfully sent to {recipients} using Flask-Mail")
            return True
            
        except Exception as flask_mail_error:
            print(f"❌ Flask-Mail error: {str(flask_mail_error)}")
            print("📧 Trying fallback with direct SMTP...")
            
            # Get email config from app for direct SMTP
            smtp_server = app.config['MAIL_SERVER']
            port = app.config['MAIL_PORT']
            username = app.config['MAIL_USERNAME']
            password = app.config['MAIL_PASSWORD']
            use_ssl = app.config.get('MAIL_USE_SSL', False)
            sender = app.config['MAIL_DEFAULT_SENDER']
            
            # Create MIME message
            mime_msg = MIMEMultipart()
            mime_msg['Subject'] = subject
            mime_msg['From'] = sender
            mime_msg['To'] = ", ".join(recipients)
            
            # Attach HTML content
            mime_msg.attach(MIMEText(msg.html, 'html'))
            
            # Connect to SMTP server
            try:
                if use_ssl:
                    print(f"📧 Connecting to {smtp_server}:{port} using SSL")
                    smtp = smtplib.SMTP_SSL(smtp_server, port)
                else:
                    print(f"📧 Connecting to {smtp_server}:{port}")
                    smtp = smtplib.SMTP(smtp_server, port)
                    if app.config.get('MAIL_USE_TLS', False):
                        smtp.starttls()
                
                # Set debug level for verbose output
                smtp.set_debuglevel(1)
                
                # Login with credentials
                print(f"📧 Logging in as {username}")
                smtp.login(username, password)
                
                # Send email
                print(f"📧 Sending email to {recipients}")
                smtp.sendmail(sender, recipients, mime_msg.as_string())
                
                # Close connection
                smtp.quit()
                print(f"✅ Email successfully sent to {recipients} using direct SMTP")
                return True
                
            except Exception as smtp_error:
                print(f"❌ Direct SMTP error: {str(smtp_error)}")
                traceback.print_exc()
                return False
                
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        traceback.print_exc()
        return False

def send_booking_confirmation_email(booking):
    """Send booking confirmation email to user"""
    if not booking.user.email:
        print("ERROR: Cannot send email - User has no email address!")
        return False
        
    subject = f"Booking Confirmation - {booking.turf.name}"
    recipients = [booking.user.email]
    
    print(f"Preparing booking confirmation email for {booking.user.email}")
    
    # Format the date and time for email
    booking_date = booking.booking_date.strftime('%A, %d %B %Y')
    start_time = booking.start_time.strftime('%I:%M %p')
    end_time = booking.end_time.strftime('%I:%M %p')
    
    success = send_email(
        subject=subject,
        recipients=recipients,
        template='emails/booking_confirmation.html',
        booking=booking,
        booking_date=booking_date,
        start_time=start_time,
        end_time=end_time,
        user=booking.user,
        turf=booking.turf
    )
    
    if success:
        print(f"✅ Booking confirmation email sent to {booking.user.email}")
    else:
        print(f"❌ Failed to send booking confirmation email to {booking.user.email}")
    
    return success

def send_booking_notification_to_owner(booking):
    """Send booking notification to turf owner"""
    if not booking.turf.owner.email:
        print("ERROR: Cannot send email - Turf owner has no email address!")
        return False
        
    subject = f"New Booking - {booking.turf.name}"
    recipients = [booking.turf.owner.email]
    
    print(f"Preparing booking notification email for turf owner {booking.turf.owner.email}")
    
    # Format the date and time for email
    booking_date = booking.booking_date.strftime('%A, %d %B %Y')
    start_time = booking.start_time.strftime('%I:%M %p')
    end_time = booking.end_time.strftime('%I:%M %p')
    
    success = send_email(
        subject=subject,
        recipients=recipients,
        template='emails/owner_booking_notification.html',
        booking=booking,
        booking_date=booking_date,
        start_time=start_time,
        end_time=end_time,
        user=booking.user,
        turf=booking.turf
    )
    
    if success:
        print(f"✅ Booking notification email sent to owner {booking.turf.owner.email}")
    else:
        print(f"❌ Failed to send booking notification email to owner {booking.turf.owner.email}")
    
    return success

def send_cancellation_notification_to_user(booking):
    """Send booking cancellation email to user"""
    if not booking.user.email:
        print("ERROR: Cannot send cancellation email - User has no email address!")
        return False
        
    subject = f"Booking Cancellation - {booking.turf.name}"
    recipients = [booking.user.email]
    
    print(f"Preparing cancellation email for {booking.user.email}")
    
    # Format the date and time for email
    booking_date = booking.booking_date.strftime('%A, %d %B %Y')
    start_time = booking.start_time.strftime('%I:%M %p')
    end_time = booking.end_time.strftime('%I:%M %p')
    
    success = send_email(
        subject=subject,
        recipients=recipients,
        template='emails/booking_cancellation.html',
        booking=booking,
        booking_date=booking_date,
        start_time=start_time,
        end_time=end_time,
        user=booking.user,
        turf=booking.turf
    )
    
    if success:
        print(f"✅ Cancellation email sent to {booking.user.email}")
    else:
        print(f"❌ Failed to send cancellation email to {booking.user.email}")
    
    return success

def send_cancellation_notification_to_owner(booking):
    """Send booking cancellation notification to turf owner"""
    if not booking.turf.owner.email:
        print("ERROR: Cannot send cancellation email - Turf owner has no email address!")
        return False
        
    subject = f"Booking Cancellation - {booking.turf.name}"
    recipients = [booking.turf.owner.email]
    
    print(f"Preparing cancellation notification email for owner {booking.turf.owner.email}")
    
    # Format the date and time for email
    booking_date = booking.booking_date.strftime('%A, %d %B %Y')
    start_time = booking.start_time.strftime('%I:%M %p')
    end_time = booking.end_time.strftime('%I:%M %p')
    
    success = send_email(
        subject=subject,
        recipients=recipients,
        template='emails/owner_cancellation_notification.html',
        booking=booking,
        booking_date=booking_date,
        start_time=start_time,
        end_time=end_time,
        user=booking.user,
        turf=booking.turf
    )
    
    if success:
        print(f"✅ Cancellation notification email sent to owner {booking.turf.owner.email}")
    else:
        print(f"❌ Failed to send cancellation notification email to owner {booking.turf.owner.email}")
    
    return success
