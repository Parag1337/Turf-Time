import mysql.connector
from mysql.connector import errorcode

# MySQL connection configuration
config = {
    'user': 'root',
    'password': 'password',  # Your MySQL Workbench password
    'host': '127.0.0.1',
    'port': 3306,
    'raise_on_warnings': True
}

# Database name
DB_NAME = 'turf_time'

# Define tables
TABLES = {}

# Users table
TABLES['users'] = (
    "CREATE TABLE `users` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `username` varchar(50) NOT NULL UNIQUE,"
    "  `email` varchar(100) NOT NULL UNIQUE,"
    "  `password` varchar(255) NOT NULL,"
    "  `role` varchar(20) NOT NULL,"
    "  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
)

# Turfs table
TABLES['turfs'] = (
    "CREATE TABLE `turfs` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(100) NOT NULL,"
    "  `location` varchar(255) NOT NULL,"
    "  `description` text,"
    "  `price_per_hour` decimal(10,2) NOT NULL,"
    "  `image_url` varchar(255),"
    "  `owner_id` int NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`)"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
)

# Bookings table
TABLES['bookings'] = (
    "CREATE TABLE `bookings` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `turf_id` int NOT NULL,"
    "  `user_id` int NOT NULL,"
    "  `booking_date` date NOT NULL,"
    "  `start_time` time NOT NULL,"
    "  `end_time` time NOT NULL,"
    "  `total_price` decimal(10,2) NOT NULL,"
    "  `status` varchar(20) NOT NULL DEFAULT 'confirmed',"
    "  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`turf_id`) REFERENCES `turfs` (`id`),"
    "  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
)

def create_database():
    """Create database and tables."""
    try:
        print("Connecting to MySQL server...")
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Invalid username or password")
        else:
            print(f"Error: {err}")
        return

    # Create database
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"Database '{DB_NAME}' created successfully.")
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")
        return

    # Use the database
    try:
        cursor.execute(f"USE {DB_NAME}")
    except mysql.connector.Error as err:
        print(f"Failed to use database: {err}")
        return

    # Create tables
    for table_name, table_sql in TABLES.items():
        try:
            print(f"Creating table {table_name}...")
            cursor.execute(table_sql)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table already exists.")
            else:
                print(f"Error creating table: {err}")
        else:
            print(f"Table '{table_name}' created successfully.")

    # Create application user
    try:
        print("Creating application user...")
        # Replace 'turf_user' and 'turf_password' with your preferred username and password
        cursor.execute("CREATE USER IF NOT EXISTS 'turf_user'@'localhost' IDENTIFIED BY 'turf_password'")
        cursor.execute(f"GRANT ALL PRIVILEGES ON {DB_NAME}.* TO 'turf_user'@'localhost'")
        cursor.execute("FLUSH PRIVILEGES")
        print("Application user created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating application user: {err}")

    cursor.close()
    conn.close()
    print("MySQL setup completed successfully!")

if __name__ == "__main__":
    create_database()