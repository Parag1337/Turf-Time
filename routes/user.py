from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from database.models import db, Turf, Booking, TeamRequest
from forms import BookingForm, TeamRequestForm
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
        else:
            # Create the booking
            booking = Booking(
                turf_id=turf.id,
                user_id=current_user.id,
                booking_date=form.booking_date.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                total_price=total_price,
                status='confirmed',
                # Player finding options
                public_booking=form.public_booking.data,
                max_players=form.max_players.data,
                notes=form.notes.data
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
            
            message_suffix = " Your booking is also listed as public for team finding." if form.public_booking.data else ""
            flash(f'Booking confirmed for {turf.name}! A confirmation email has been {email_status} to your registered email address.{message_suffix}', 'success')
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

@user_bp.route('/find_teams')
@login_required
def find_teams():
    # Find public bookings that are in the future and still confirmed
    today = datetime.now().date()
    public_bookings = Booking.query.filter(
        Booking.public_booking == True,
        Booking.booking_date >= today,
        Booking.status == 'confirmed'
    ).order_by(Booking.booking_date, Booking.start_time).all()
    
    # Filter out bookings that the current user has already requested to join
    requested_booking_ids = [req.booking_id for req in TeamRequest.query.filter_by(requester_id=current_user.id).all()]
    
    # Filter out the user's own bookings
    available_bookings = [b for b in public_bookings if b.user_id != current_user.id and b.id not in requested_booking_ids]
    
    return render_template('user/find_teams.html', 
                          title='Find Teams', 
                          bookings=available_bookings,
                          now=datetime.now)


@user_bp.route('/join_team/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def join_team(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    # Make sure it's a public booking
    if not booking.public_booking:
        flash("This booking is not open for team requests.", "danger")
        return redirect(url_for('user.find_teams'))
    
    # Make sure it's not the user's own booking
    if booking.user_id == current_user.id:
        flash("You can't join your own booking.", "danger")
        return redirect(url_for('user.find_teams'))
    
    # Check if user already sent a request
    existing_request = TeamRequest.query.filter_by(
        booking_id=booking.id,
        requester_id=current_user.id
    ).first()
    
    if existing_request:
        flash("You have already sent a request to join this team.", "info")
        return redirect(url_for('user.find_teams'))
    
    form = TeamRequestForm()
    
    if form.validate_on_submit():
        team_request = TeamRequest(
            booking_id=booking.id,
            requester_id=current_user.id,
            message=form.message.data,
            status='pending'
        )
        db.session.add(team_request)
        db.session.commit()
        
        flash("Request sent successfully! You'll be notified when the organizer responds.", "success")
        return redirect(url_for('user.my_team_requests'))
    
    return render_template('user/join_team.html',
                          title='Join Team',
                          booking=booking,
                          form=form)


@user_bp.route('/my_team_requests')
@login_required
def my_team_requests():
    # Get requests made by the current user
    sent_requests = TeamRequest.query.filter_by(requester_id=current_user.id).all()
    
    # Get requests for the user's bookings
    user_bookings = [b.id for b in Booking.query.filter_by(user_id=current_user.id).all()]
    received_requests = TeamRequest.query.filter(TeamRequest.booking_id.in_(user_bookings)).all()
    
    return render_template('user/my_team_requests.html',
                          title='My Team Requests',
                          sent_requests=sent_requests,
                          received_requests=received_requests)


@user_bp.route('/respond_team_request/<int:request_id>/<string:action>', methods=['POST'])
@login_required
def respond_team_request(request_id, action):
    team_request = TeamRequest.query.get_or_404(request_id)
    
    # Make sure the request is for a booking owned by the current user
    if team_request.booking.user_id != current_user.id:
        flash("You don't have permission to respond to this request.", "danger")
        return redirect(url_for('user.my_team_requests'))
    
    if action == 'accept':
        team_request.status = 'accepted'
        db.session.commit()
        flash(f"You've accepted the request from {team_request.requester.username} to join your team.", "success")
    
    elif action == 'reject':
        team_request.status = 'rejected'
        db.session.commit()
        flash(f"You've rejected the request from {team_request.requester.username}.", "info")
    
    return redirect(url_for('user.my_team_requests'))