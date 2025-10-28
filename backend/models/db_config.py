import mysql.connector
from mysql.connector import Error
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path to import network_utils
sys.path.append(str(Path(__file__).parent.parent))
from services.network_utils import get_local_ip

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def get_db_host():
    """
    Get database host from environment or use device's local IP.
    """
    host = os.getenv('MYSQL_HOST', None)
    
    # If MYSQL_HOST is not set or is set to 'auto', use device IP
    if not host or host.lower() == 'auto':
        return get_local_ip()
    
    return host

def get_db_connection():
    """
    Create and return a MySQL database connection.
    Reads credentials from environment variables.
    Returns None if connection fails.
    """
    try:
        host = get_db_host()
        connection = mysql.connector.connect(
            host=host,
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DB', 'landwand_db'),
            port=int(os.getenv('MYSQL_PORT', '3306')),
            autocommit=True
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Successfully connected to MySQL Server at {host} (version {db_info})")
            return connection
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def close_db_connection(connection):
    """
    Close the database connection safely.
    """
    if connection and connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

def test_connection():
    """
    Test the database connection.
    Returns True if successful, False otherwise.
    """
    conn = get_db_connection()
    if conn:
        close_db_connection(conn)
        return True
    return False
