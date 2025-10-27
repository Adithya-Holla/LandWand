"""
MySQL Connection Test Script
Tests various connection scenarios to help diagnose connectivity issues.
"""

import mysql.connector
from mysql.connector import Error
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add backend directory to path to import network_utils
sys.path.append(str(Path(__file__).parent.parent / 'backend'))
from services.network_utils import get_local_ip

# Load environment variables from backend/.env
env_path = Path(__file__).parent.parent / 'backend' / '.env'
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

def test_connection(host, user, password, port=3306, timeout=5):
    """Test MySQL connection with given parameters."""
    try:
        print(f"\n{'='*60}")
        print(f"Testing connection to: {host}:{port}")
        print(f"User: {user}")
        print(f"Timeout: {timeout} seconds")
        print('='*60)
        
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            connection_timeout=timeout
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✅ SUCCESS! Connected to MySQL Server version {db_info}")
            
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"   Database version: {version[0]}")
            
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print(f"   Available databases: {len(databases)}")
            for db in databases:
                print(f"      - {db[0]}")
            
            cursor.close()
            connection.close()
            return True
    
    except Error as e:
        print(f"❌ FAILED: {e}")
        
        # Provide specific error guidance
        error_code = e.errno if hasattr(e, 'errno') else None
        
        if error_code == 2003:
            print("\n💡 Error 2003: Can't connect to MySQL server")
            print("   Possible causes:")
            print("   • MySQL server is not running")
            print("   • Firewall blocking port 3306")
            print("   • Wrong host/IP address")
            print("   • Network connectivity issues")
        elif error_code == 1045:
            print("\n💡 Error 1045: Access denied")
            print("   Possible causes:")
            print("   • Wrong username or password")
            print("   • User doesn't have permission to connect from this host")
        elif error_code == 2005:
            print("\n💡 Error 2005: Unknown MySQL server host")
            print("   Possible causes:")
            print("   • Invalid hostname or IP address")
            print("   • DNS resolution issues")
        
        return False
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🔍 MySQL Connection Diagnostic Tool")
    print("="*60)
    
    # Show device IP
    device_ip = get_local_ip()
    print(f"\n📍 Your Device IP: {device_ip}")
    
    # Test 1: Environment variables from .env
    print("\n📋 Test 1: Using credentials from .env file")
    host = get_db_host()
    user = os.getenv('MYSQL_USER', 'root')
    password = os.getenv('MYSQL_PASSWORD', '')
    port = int(os.getenv('MYSQL_PORT', '3306'))
    
    print(f"   MYSQL_HOST from .env: {os.getenv('MYSQL_HOST', 'not set')}")
    print(f"   Resolved host: {host}")
    
    if not password:
        print("⚠️  Warning: MYSQL_PASSWORD is empty in .env file")
    
    success1 = test_connection(host, user, password, port, timeout=10)
    
    # Test 2: Try localhost if remote connection failed
    if not success1 and host != 'localhost':
        print("\n\n📋 Test 2: Trying localhost connection")
        print("   (Testing if MySQL is installed locally)")
        success2 = test_connection('localhost', user, password, port, timeout=5)
        
        if success2:
            print("\n✅ Local MySQL connection works!")
            print("💡 Consider using localhost instead of remote server")
            print("   Update MYSQL_HOST=localhost in your .env file")
    
    # Test 3: Try 127.0.0.1 instead of localhost
    if not success1 and host == 'localhost':
        print("\n\n📋 Test 3: Trying 127.0.0.1 instead of localhost")
        success3 = test_connection('127.0.0.1', user, password, port, timeout=5)
    
    # Final recommendations
    print("\n" + "="*60)
    print("📝 Recommendations")
    print("="*60)
    
    if success1:
        print("✅ Connection successful! You're ready to run init_db.py")
    else:
        print("\n❌ Connection failed. Please check:")
        print("\n1. Is MySQL installed and running?")
        print("   Windows: Check Services (services.msc) for MySQL")
        print("   Or install: https://dev.mysql.com/downloads/mysql/")
        
        print("\n2. Verify your .env file contains correct credentials:")
        print(f"   Current .env location: backend/.env")
        print(f"   MYSQL_HOST={host}")
        print(f"   MYSQL_USER={user}")
        print(f"   MYSQL_PASSWORD=[hidden]")
        print(f"   MYSQL_PORT={port}")
        
        print("\n3. For remote MySQL servers:")
        print("   • Ensure the server allows remote connections")
        print("   • Check firewall rules (port 3306)")
        print("   • Verify user has remote access privileges:")
        print(f"     mysql> CREATE USER '{user}'@'%' IDENTIFIED BY 'password';")
        print(f"     mysql> GRANT ALL PRIVILEGES ON *.* TO '{user}'@'%';")
        
        print("\n4. Test MySQL CLI connection:")
        print(f"   mysql -h {host} -P {port} -u {user} -p")
        
        print("\n5. Consider using a local MySQL installation:")
        print("   • Download: https://dev.mysql.com/downloads/mysql/")
        print("   • Or use XAMPP/WAMP which includes MySQL")
        print("   • Then set MYSQL_HOST=localhost in .env")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
