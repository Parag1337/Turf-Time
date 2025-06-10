from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from database.models import db, Turf, Booking
from forms import BookingForm

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
                status='confirmed'
            )
            
            db.session.add(booking)
            db.session.commit()
            
            flash(f'Booking confirmed for {turf.name}!', 'success')
            return redirect(url_for('user.my_bookings'))
    
    return render_template('user/book_turf.html', 
                          title=f'Book {turf.name}', 
                          turf=turf, 
                          form=form)