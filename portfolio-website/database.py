import pymysql
from pymysql.cursors import DictCursor
from config import Config
from contextlib import contextmanager

@contextmanager
def db_connection():
    """Context manager for database connections"""
    conn = None
    try:
        conn = pymysql.connect(**Config.DB_CONFIG)
        yield conn
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def test_connection():
    """Test database connection"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                result = cursor.fetchone()
                print(f"✅ Database connection successful! MySQL version: {result['VERSION()']}")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

# Test connection when module is run directly
if __name__ == "__main__":
    test_connection()