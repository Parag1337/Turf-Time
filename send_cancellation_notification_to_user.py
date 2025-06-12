def send_cancellation_notification_to_user(booking):
    """Send booking cancellation email to user"""
    if not booking.user.email:
        print("ERROR: Cannot send cancellation email - User has no email address!")
        return False
        
    subject = f"Booking Cancellation - {booking.turf.name}"
    recipients = [booking.user.email]
    
    print(f"DEBUG: Preparing cancellation email for user {booking.user.email}")
    print(f"DEBUG: User ID: {booking.user.id}, Username: {booking.user.username}")
    print(f"DEBUG: Turf name: {booking.turf.name}")
    
    # Format the date and time for email
    booking_date = booking.booking_date.strftime('%A, %d %B %Y')
    start_time = booking.start_time.strftime('%I:%M %p')
    end_time = booking.end_time.strftime('%I:%M %p')
    
    print(f"DEBUG: Formatted date/time - Date: {booking_date}, Time: {start_time} to {end_time}")
    
    try:
        print(f"DEBUG: Attempting to send cancellation email with template 'emails/booking_cancellation.html'")
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
            print(f" Cancellation email sent to {booking.user.email}")
        else:
            print(f" Failed to send cancellation email to {booking.user.email}")
        
        return success
    except Exception as e:
        print(f" EXCEPTION during cancellation email sending: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
