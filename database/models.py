from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'owner'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Profile fields
    bio = db.Column(db.Text)
    phone = db.Column(db.String(20))
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True)
    turfs = db.relationship('Turf', backref='owner', lazy=True)
    # Note: team_requests relationship is defined in the TeamRequest model
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def is_owner(self):
        return self.role == 'owner'
    
    def __repr__(self):
        return f'<User {self.username}>'


class Turf(db.Model):
    __tablename__ = 'turfs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price_per_hour = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    bookings = db.relationship('Booking', backref='turf', lazy=True)
    
    def __repr__(self):
        return f'<Turf {self.name}>'


class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    turf_id = db.Column(db.Integer, db.ForeignKey('turfs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='confirmed')  # 'confirmed', 'cancelled', 'completed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Player finding system fields
    public_booking = db.Column(db.Boolean, default=False)
    max_players = db.Column(db.Integer, default=0)  # 0 means no limit set
    current_players = db.Column(db.Integer, default=1)  # Default is 1 (the booking creator)
    notes = db.Column(db.Text)
    
    # Relationships
    team_requests = db.relationship('TeamRequest', backref='booking', lazy=True)
    
    def __repr__(self):
        return f'<Booking {self.id}>'


class TeamRequest(db.Model):
    __tablename__ = 'team_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'rejected'
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with User (requester)
    requester = db.relationship('User', backref='team_requests')
    
    def __repr__(self):
        return f'<TeamRequest {self.id}>'