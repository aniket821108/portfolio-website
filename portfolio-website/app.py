from flask import Flask, render_template, request, jsonify
import pymysql.cursors
import os
from config import Config

app = Flask(__name__)

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'aniket123@',  # Consider using environment variables
    'database': 'portfolio_db',  # Changed from airline_booking to match your needs
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    """Establish and return a new database connection"""
    return pymysql.connect(**DB_CONFIG)

# Verify database connection at startup
try:
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("✅ Database connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    raise RuntimeError("Database connection failed") from e

# Create database tables if they don't exist
def create_tables():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Create messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create projects table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(100) NOT NULL,
                    description TEXT NOT NULL,
                    tags VARCHAR(255),
                    image VARCHAR(100)
                )
            """)
        conn.commit()
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        conn.close()

create_tables()

# Sample data (you can load this from database)
projects = [
    {
        'id': 1,
        'title': 'airline_booking',
        'description': 'A web application for booking airline tickets.',
        'tags': ['Python', 'Flask', 'JavaScript'],
        'image': 'project1.jpg'
    }
]

skills = [
    {'name': 'Python', 'level': 90},
    {'name': 'Flask', 'level': 85},
    {'name': 'JavaScript', 'level': 80},
    {'name': 'HTML/CSS', 'level': 75},
    {'name': 'MySQL', 'level': 70}
]

@app.route('/')
def home():
    return render_template('index.html', projects=projects, skills=skills)

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
                    (name, email, message)
                )
            conn.commit()
            
            return jsonify({
                'success': True,
                'message': 'Thank you for your message!'
            })
            
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({
                'success': False,
                'message': 'There was an error submitting your message.'
            }), 500
        finally:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)