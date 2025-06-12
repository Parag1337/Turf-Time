"""
This is a utility script to fix the indentation in email_utils.py
"""

# Read the entire content of email_utils.py
with open('utils/email_utils.py', 'r') as file:
    content = file.read()

# Replace the problematic section
problematic = """    print(f"DEBUG: Formatted date/time - Date: {booking_date}, Time: {start_time} to {end_time}")
      try:
        print(f"DEBUG: Attempting to send cancellation email with template 'emails/booking_cancellation.html'")"""

fixed = """    print(f"DEBUG: Formatted date/time - Date: {booking_date}, Time: {start_time} to {end_time}")
    
    try:
        print(f"DEBUG: Attempting to send cancellation email with template 'emails/booking_cancellation.html'")"""

# Replace the content
fixed_content = content.replace(problematic, fixed)

# Write the fixed content back to the file
with open('utils/email_utils.py', 'w') as file:
    file.write(fixed_content)

print("Fixed the indentation in email_utils.py successfully!")
