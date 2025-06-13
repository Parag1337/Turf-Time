from app import create_app
from database.models import db, Booking
from sqlalchemy import text
import sys

def check_column_exists():
    """Check if current_players column exists in the database"""
    print("Checking if current_players column exists...")
    
    app = create_app()
    with app.app_context():
        # Check if the column exists
        try:
            result = db.session.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'bookings' 
                AND COLUMN_NAME = 'current_players'
            """))
            count = result.scalar()
            
            if count == 0:
                print("ERROR: The 'current_players' column doesn't exist in the bookings table.")
                print("Please run 'python update_schema.py' first to add the column.")
                return False
                
            return True
        except Exception as e:
            print(f"Error checking for column: {str(e)}")
            return False

def update_current_players():
    """
    Update all existing bookings to have a current_players value of 1
    """
    print("Updating current_players for existing bookings...")
    
    # First check if the column exists
    if not check_column_exists():
        sys.exit(1)
        
    app = create_app()
    with app.app_context():
        try:
            # Use raw SQL to update all NULL values to 1
            db.session.execute(text("""
                UPDATE bookings 
                SET current_players = 1 
                WHERE current_players IS NULL
            """))
            
            # Commit the changes
            db.session.commit()
            print("Successfully updated bookings with default current_players value.")
        except Exception as e:
            print(f"Error updating bookings: {str(e)}")
            db.session.rollback()
            sys.exit(1)
            
if __name__ == "__main__":
    update_current_players()
