from flask import Flask
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object('config.Config')

# Mock objects for testing
class MockUser:
    def __init__(self):
        self.id = 1
        self.username = "test_user"
        self.email = "test@example.com"

class MockTurf:
    def __init__(self):
        self.id = 1
        self.name = "Test Turf"
        self.location = "Test Location"
        self.owner = MockUser()

class MockBooking:
    def __init__(self):
        self.id = 123
        self.user = MockUser()
        self.turf = MockTurf()
        self.booking_date = datetime.now().date()
        self.start_time = datetime.now().replace(hour=10, minute=0)
        self.end_time = datetime.now().replace(hour=11, minute=0)
        self.total_price = 1000
        self.status = "cancelled"

def test_template(template_path):
    """Test if a template can be rendered"""
    print(f"Testing template: {template_path}")
    
    with app.app_context():
        from utils.email_utils import send_email
        
        # Use a fixed date/time to avoid now() function issues
        booking_date = datetime.now().strftime('%A, %d %B %Y')
        start_time = "10:00 AM"
        end_time = "11:00 AM"
        
        # Create mock objects
        booking = MockBooking()
        user = booking.user
        turf = booking.turf
        
        try:
            # Use sender's email as recipient for testing
            recipients = [app.config['MAIL_USERNAME']]
            success = send_email(
                subject=f"TEST - Template {template_path}",
                recipients=recipients,
                template=template_path,
                booking=booking,
                booking_date=booking_date,
                start_time=start_time,
                end_time=end_time,
                user=user,
                turf=turf
            )
            if success:
                print(f"✅ Success! Email template {template_path} was rendered and sent.")
            else:
                print(f"❌ Failed to send email with template {template_path}.")
        except Exception as e:
            print(f"❌ Error rendering template {template_path}: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print("Testing email templates...")
    
    # Test all email templates
    test_template('emails/booking_confirmation.html')
    test_template('emails/booking_cancellation.html')
    test_template('emails/owner_booking_notification.html')
    test_template('emails/owner_cancellation_notification.html')
    
    print("Testing complete!")
