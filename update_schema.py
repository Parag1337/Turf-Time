import sys
import traceback
from sqlalchemy.exc import SQLAlchemyError
from app import create_app
from database.models import db, User, TeamRequest
from sqlalchemy import text

try:
    print("Creating application context...")
    app = create_app()
    
    with app.app_context():
        print("Adding team finding columns to database schema...")
        
        # MySQL-specific approach with proper error handling
        try:
            print("- Adding 'public_booking' column to bookings table...")
            db.session.execute(text("ALTER TABLE bookings ADD COLUMN public_booking TINYINT(1) DEFAULT 0"))
            print("  Column added successfully")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("  Column 'public_booking' already exists, skipping")
            else:
                print(f"  Error: {str(e)}")
        
        try:
            print("- Adding 'max_players' column to bookings table...")
            db.session.execute(text("ALTER TABLE bookings ADD COLUMN max_players INT DEFAULT 0"))
            print("  Column added successfully")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("  Column 'max_players' already exists, skipping")
            else:
                print(f"  Error: {str(e)}")
        
        try:
            print("- Adding 'current_players' column to bookings table...")
            db.session.execute(text("ALTER TABLE bookings ADD COLUMN current_players INT DEFAULT 1"))
            print("  Column added successfully")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("  Column 'current_players' already exists, skipping")
            else:
                print(f"  Error: {str(e)}")
        
        try:
            print("- Adding 'notes' column to bookings table...")
            db.session.execute(text("ALTER TABLE bookings ADD COLUMN notes TEXT"))
            print("  Column added successfully")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("  Column 'notes' already exists, skipping")
            else:
                print(f"  Error: {str(e)}")
        
        # Add new fields to User table
        try:
            print("- Adding 'bio' column to users table...")
            db.session.execute(text("ALTER TABLE users ADD COLUMN bio TEXT"))
            print("  Column added successfully")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("  Column 'bio' already exists, skipping")
            else:
                print(f"  Error: {str(e)}")
        
        try:
            print("- Adding 'phone' column to users table...")
            db.session.execute(text("ALTER TABLE users ADD COLUMN phone VARCHAR(20)"))
            print("  Column added successfully")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("  Column 'phone' already exists, skipping")
            else:
                print(f"  Error: {str(e)}")
        
        # Create TeamRequest table
        print("- Creating team_requests table...")
        try:
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS team_requests (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    booking_id INT NOT NULL,
                    requester_id INT NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending',
                    message TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (booking_id) REFERENCES bookings (id),
                    FOREIGN KEY (requester_id) REFERENCES users (id)
                )
            """))
            print("  Table created successfully")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("  Table 'team_requests' already exists, skipping")
            else:
                print(f"  Error: {str(e)}")
          # Commit the changes
        print("Committing changes...")
        db.session.commit()
        print("Database schema updated successfully!")
                
except Exception as e:
    print(f"Error: {str(e)}")
    traceback.print_exc()
    sys.exit(1)
