from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from werkzeug.utils import secure_filename
import os
from database.models import db, Turf, Booking
from forms import TurfForm, FilterBookingsForm

owner_bp = Blueprint('owner', __name__, url_prefix='/owner')

def owner_required(f):
    """Decorator to check if user is an owner"""
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_owner():
            flash("Access denied. You must be a turf owner to access this page.", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@owner_bp.route('/dashboard')
@owner_required
def dashboard():
    # Get all turfs owned by the current user
    turfs = Turf.query.filter_by(owner_id=current_user.id).all()
    
    # Get all bookings for those turfs
    turf_ids = [turf.id for turf in turfs]
    
    # If user has no turfs yet, return empty dashboard
    if not turf_ids:
        return render_template('owner/dashboard.html', 
                              title='Owner Dashboard', 
                              turfs=[], 
                              bookings=[], 
                              total_bookings=0, 
                              upcoming_bookings=0, 
                              monthly_earnings=0)
    
    bookings = Booking.query.filter(Booking.turf_id.in_(turf_ids)).all()
    
    # Calculate statistics
    today = datetime.now().date()
    month_start = datetime(today.year, today.month, 1).date()
    upcoming_bookings = sum(1 for b in bookings if b.booking_date >= today and b.status == 'confirmed')
    
    # Calculate monthly earnings
    monthly_earnings = sum(b.total_price for b in bookings 
                        if b.booking_date >= month_start 
                        and b.booking_date <= today
                        and b.status != 'cancelled')
    
    return render_template('owner/dashboard.html', 
                          title='Owner Dashboard', 
                          turfs=turfs, 
                          bookings=bookings, 
                          total_bookings=len(bookings), 
                          upcoming_bookings=upcoming_bookings, 
                          monthly_earnings=monthly_earnings)

@owner_bp.route('/my_turfs')
@owner_required
def my_turfs():
    turfs = Turf.query.filter_by(owner_id=current_user.id).all()
    return render_template('owner/my_turfs.html', title='My Turfs', turfs=turfs)

@owner_bp.route('/add_turf', methods=['GET', 'POST'])
@owner_required
def add_turf():
    form = TurfForm()
    
    if form.validate_on_submit():        # Handle image upload if provided
        image_url = None
        if form.image.data and form.image.data.filename:
            filename = secure_filename(form.image.data.filename)
            # Create uploads folder if it doesn't exist
            upload_folder = os.path.join('static', 'uploads', 'turfs')
            os.makedirs(upload_folder, exist_ok=True)
            
            # Save the file
            filepath = os.path.join(upload_folder, filename)
            form.image.data.save(filepath)
            
            # Store the path relative to static folder using forward slashes for URL compatibility
            image_url = 'uploads/turfs/' + filename
            
            print(f"Saved image to {filepath}, DB will store: {image_url}")
        
        # Create new turf
        turf = Turf(
            name=form.name.data,
            location=form.location.data,
            description=form.description.data,
            price_per_hour=form.price_per_hour.data,
            image_url=image_url,
            owner_id=current_user.id
        )
        
        db.session.add(turf)
        db.session.commit()
        
        flash(f'{turf.name} added successfully!', 'success')
        return redirect(url_for('owner.my_turfs'))
    
    return render_template('owner/add_turf.html', title='Add Turf', form=form)

@owner_bp.route('/view_bookings')
@owner_required
def view_bookings():
    form = FilterBookingsForm()
    
    # Get turfs owned by current user for the filter dropdown
    turfs = Turf.query.filter_by(owner_id=current_user.id).all()
    form.turf.choices = [('all', 'All Turfs')] + [(str(t.id), t.name) for t in turfs]
    
    # Get filter parameters
    selected_turf = request.args.get('turf', 'all')
    selected_status = request.args.get('status', 'all')
    
    # Parse dates from parameters or use defaults
    try:
        date_from = datetime.strptime(request.args.get('date_from', ''), '%Y-%m-%d').date()
    except (ValueError, TypeError):
        date_from = datetime.now().date() - timedelta(days=30)  # Default to last 30 days
        
    try:
        date_to = datetime.strptime(request.args.get('date_to', ''), '%Y-%m-%d').date()
    except (ValueError, TypeError):
        date_to = datetime.now().date() + timedelta(days=30)  # Default to next 30 days
    
    # Set form values
    form.turf.data = selected_turf
    form.status.data = selected_status
    form.date_from.data = date_from
    form.date_to.data = date_to
    
    # Build query based on filters
    query = Booking.query.join(Turf).filter(Turf.owner_id == current_user.id)
    
    if selected_turf != 'all':
        query = query.filter(Booking.turf_id == selected_turf)
    
    if selected_status != 'all':
        query = query.filter(Booking.status == selected_status)
    
    query = query.filter(and_(
        Booking.booking_date >= date_from,
        Booking.booking_date <= date_to
    ))
    
    # Get bookings
    bookings = query.order_by(Booking.booking_date.desc(), Booking.start_time.desc()).all()
    
    return render_template('owner/bookings.html', 
                          title='Bookings', 
                          form=form,
                          bookings=bookings, 
                          turfs=turfs,
                          selected_status=selected_status,
                          selected_turf=selected_turf, 
                          date_from=date_from, 
                          date_to=date_to)