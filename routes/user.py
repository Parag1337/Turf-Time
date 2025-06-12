from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from database.models import db, Turf, Booking
from forms import BookingForm
from utils.email_utils import (
    send_booking_confirmation_email,
    send_booking_notification_to_owner,
    send_cancellation_notification_to_user,
    send_cancellation_notification_to_owner
)
import logging

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/dashboard')
@login_required
def dashboard():
    # Get recent bookings for the user
    recent_bookings = Booking.query.filter_by(user_id=current_user.id)\
        .order_by(Booking.created_at.desc()).limit(5).all()
    
    return render_template('user/dashboard.html', 
                          title='User Dashboard', 
                          bookings=recent_bookings, 
                          now=datetime.now)

@user_bp.route('/view_turfs')
@login_required
def view_turfs():
    # Get all available turfs
    turfs = Turf.query.all()
    
    return render_template('user/view_turfs.html', 
                          title='Available Turfs', 
                          turfs=turfs)

@user_bp.route('/my_bookings')
@login_required
def my_bookings():
    # Get all bookings for the current user
    bookings = Booking.query.filter_by(user_id=current_user.id)\
        .order_by(Booking.booking_date.desc(), Booking.start_time.desc()).all()
    
    return render_template('user/my_bookings.html', 
                          title='My Bookings', 
                          bookings=bookings, 
                          now=datetime.now)

@user_bp.route('/book_turf/<int:turf_id>', methods=['GET', 'POST'])
@login_required
def book_turf(turf_id):
    turf = Turf.query.get_or_404(turf_id)
    form = BookingForm()
    
    # Set default date to tomorrow
    if request.method == 'GET':
        form.booking_date.data = datetime.now().date() + timedelta(days=1)
    
    if form.validate_on_submit():
        # Calculate total price based on duration (in hours)
        start_datetime = datetime.combine(form.booking_date.data, form.start_time.data)
        end_datetime = datetime.combine(form.booking_date.data, form.end_time.data)
        duration = (end_datetime - start_datetime).total_seconds() / 3600  # hours
        total_price = duration * turf.price_per_hour
        
        # Check for booking conflicts
        conflicting_bookings = Booking.query.filter(
            Booking.turf_id == turf.id,
            Booking.booking_date == form.booking_date.data,
            Booking.status == 'confirmed',
            ((Booking.start_time <= form.start_time.data) & (Booking.end_time > form.start_time.data)) |
            ((Booking.start_time < form.end_time.data) & (Booking.end_time >= form.end_time.data)) |
            ((Booking.start_time >= form.start_time.data) & (Booking.end_time <= form.end_time.data))
        ).all()
        
        if conflicting_bookings:
            flash('This time slot is already booked. Please choose a different time.', 'danger')
        else:            # Create the booking
            booking = Booking(
                turf_id=turf.id,
                user_id=current_user.id,
                booking_date=form.booking_date.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                total_price=total_price,
                status='confirmed'
            )
            db.session.add(booking)
            db.session.commit()
              # Send confirmation emails with improved error handling
            email_status = "sent"
            try:
                # Log detailed information about the booking and emails
                print(f"\n----- BOOKING EMAIL ATTEMPT -----")
                print(f"Attempting to send booking confirmation emails...")
                print(f"User ID: {booking.user.id}, Username: {booking.user.username}")
                print(f"User email: {booking.user.email}")
                print(f"Turf ID: {booking.turf.id}, Turf name: {booking.turf.name}")
                print(f"Owner ID: {booking.turf.owner.id}, Owner name: {booking.turf.owner.username}")
                print(f"Owner email: {booking.turf.owner.email}")
                  # Log mail configuration from current_app
                print(f"Mail server: {current_app.config['MAIL_SERVER']}")
                print(f"Mail port: {current_app.config['MAIL_PORT']}")
                print(f"Mail username: {current_app.config['MAIL_USERNAME']}")
                
                # Validate user and owner emails
                if not booking.user.email:
                    print("WARNING: User has no email address!")
                if not booking.turf.owner.email:
                    print("WARNING: Turf owner has no email address!")
                
                # Send emails with success tracking
                print("Sending confirmation email to user...")
                user_email_success = send_booking_confirmation_email(booking)
                
                print("Sending notification email to owner...")
                owner_email_success = send_booking_notification_to_owner(booking)
                
                if user_email_success and owner_email_success:
                    print("✅ All emails sent successfully")
                    email_status = "success"
                else:
                    print("⚠️ Some emails failed to send")
                    email_status = "partial"
            except Exception as e:
                # Log the error but don't prevent the booking confirmation
                import traceback
                email_status = "failed"
                print(f"Error sending email: {str(e)}")
                traceback.print_exc()
            
            flash(f'Booking confirmed for {turf.name}! A confirmation email has been {email_status} to your registered email address.', 'success')
            return redirect(url_for('user.my_bookings'))
    
    return render_template('user/book_turf.html', 
                          title=f'Book {turf.name}', 
                          turf=turf, 
                          form=form)

@user_bp.route('/cancel_booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    # Check if the booking belongs to current user
    if booking.user_id != current_user.id:
        flash('You do not have permission to cancel this booking.', 'danger')
        return redirect(url_for('user.my_bookings'))
    
    # Check if the booking is already cancelled
    if booking.status == 'cancelled':
        flash('This booking is already cancelled.', 'info')
        return redirect(url_for('user.my_bookings'))
    
    # Check if the booking date is in the past
    if booking.booking_date < datetime.now().date():
        flash('Cannot cancel past bookings.', 'danger')
        return redirect(url_for('user.my_bookings'))
      # Cancel the booking
    booking.status = 'cancelled'
    db.session.commit()    # Send cancellation emails
    try:
        user_email_success = send_cancellation_notification_to_user(booking)
        owner_email_success = send_cancellation_notification_to_owner(booking)
        
        if not (user_email_success and owner_email_success):
            print("Warning: Some cancellation emails failed to send")
    except Exception as e:
        # Log the error but don't prevent the cancellation confirmation
        print(f"Error sending cancellation emails: {str(e)}")
        import traceback
        traceback.print_exc()
    
    flash('Your booking has been cancelled successfully. A cancellation confirmation has been sent to your email.', 'success')
    return redirect(url_for('user.my_bookings'))