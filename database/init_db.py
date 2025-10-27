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

def get_db_connection():
    """
    Create and return a MySQL database connection.
    """
    try:
        host = get_db_host()
        user = os.getenv('MYSQL_USER', 'root')
        password = os.getenv('MYSQL_PASSWORD', '')
        port = int(os.getenv('MYSQL_PORT', '3306'))
        
        print(f"   Attempting connection to {host}...")
        print(f"   Using user: {user}")
        
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            connection_timeout=10,  # 10 second timeout
            autocommit=True
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✅ Successfully connected to MySQL Server version {db_info}")
            return connection
            
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        print("\n💡 Troubleshooting Tips:")
        print("   1. Check if MySQL server is running")
        print("   2. Verify host/IP address is correct")
        print("   3. Ensure port 3306 is not blocked by firewall")
        print("   4. For remote servers, ensure MySQL allows remote connections")
        print("   5. Verify username and password are correct")
        print(f"   6. Try: mysql -h {os.getenv('MYSQL_HOST')} -u {os.getenv('MYSQL_USER')} -p")
        return None

def create_database(connection, db_name):
    """
    Create database if it doesn't exist.
    """
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"✅ Database '{db_name}' is ready")
        cursor.execute(f"USE {db_name}")
        print(f"✅ Using database '{db_name}'")
        cursor.close()
        return True
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def execute_sql_file(connection, file_path):
    """
    Execute SQL statements from a file.
    Handles multi-statement scripts.
    """
    cursor = None
    try:
        # Read SQL file
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        if not sql_script.strip():
            print(f"⚠️  Warning: {file_path.name} is empty")
            return True
        
        cursor = connection.cursor()
        
        # Split SQL script into individual statements
        # Remove comments and split by semicolon
        statements = []
        current_statement = []
        
        for line in sql_script.split('\n'):
            # Skip empty lines and comments
            stripped = line.strip()
            if not stripped or stripped.startswith('--'):
                continue
            
            current_statement.append(line)
            
            # Check if statement ends with semicolon
            if stripped.endswith(';'):
                statement = '\n'.join(current_statement).strip()
                if statement:
                    statements.append(statement)
                current_statement = []
        
        # Execute each statement
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
        
        print(f"✅ Successfully executed: {file_path.name}")
        return True
        
    except Error as e:
        print(f"❌ Error executing {file_path.name}: {e}")
        return False
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error executing {file_path.name}: {e}")
        return False
        
    finally:
        if cursor:
            cursor.close()

def initialize_database():
    """
    Initialize the database by executing all SQL files in order.
    """
    print("\n" + "="*60)
    print("🚀 Starting Database Initialization")
    print("="*60 + "\n")
    
    # Display loaded configuration
    print("📋 Configuration from .env file:")
    print(f"   MYSQL_HOST: {os.getenv('MYSQL_HOST', 'not set')}")
    print(f"   MYSQL_PORT: {os.getenv('MYSQL_PORT', '3306')}")
    print(f"   MYSQL_USER: {os.getenv('MYSQL_USER', 'root')}")
    print(f"   MYSQL_PASSWORD: {'*' * len(os.getenv('MYSQL_PASSWORD', '')) if os.getenv('MYSQL_PASSWORD') else '(empty)'}")
    print(f"   MYSQL_DB: {os.getenv('MYSQL_DB', 'landwand')}\n")
    
    # Get database configuration
    db_name = os.getenv('MYSQL_DB', 'landwand')
    
    # Define the directory containing SQL files
    current_dir = Path(__file__).parent
    
    # Define SQL files in execution order
    sql_files = [
        'Landwand_db_ddl.sql',      # 1. Create tables (DDL)
        'landwand_db_dml.sql',      # 2. Insert data (DML)
        'functions.sql',            # 3. Create functions
        'triggers.sql',             # 4. Create triggers
        'procedures.sql'            # 5. Create stored procedures
    ]
    
    connection = None
    
    try:
        # Step 1: Connect to MySQL
        print("Step 1: Connecting to MySQL...")
        connection = get_db_connection()
        
        if not connection:
            print("\n❌ Failed to connect to MySQL. Please check your credentials.")
            return False
        
        # Step 2: Create and use database
        print(f"\nStep 2: Setting up database '{db_name}'...")
        if not create_database(connection, db_name):
            return False
        
        # Step 3: Execute SQL files in order
        print("\nStep 3: Executing SQL files...\n")
        
        success_count = 0
        failed_files = []
        
        for sql_file in sql_files:
            file_path = current_dir / sql_file
            print(f"  → Executing {sql_file}...", end=' ')
            
            if execute_sql_file(connection, file_path):
                success_count += 1
            else:
                failed_files.append(sql_file)
        
        # Step 4: Summary
        print("\n" + "="*60)
        print("📊 Initialization Summary")
        print("="*60)
        print(f"Total files: {len(sql_files)}")
        print(f"✅ Successful: {success_count}")
        print(f"❌ Failed: {len(failed_files)}")
        
        if failed_files:
            print(f"\nFailed files:")
            for file in failed_files:
                print(f"  - {file}")
            return False
        else:
            print("\n🎉 Database initialization completed successfully!")
            return True
        
    except Exception as e:
        print(f"\n❌ Fatal error during initialization: {e}")
        return False
        
    finally:
        # Step 5: Close connection
        if connection and connection.is_connected():
            connection.close()
            print("\n✅ MySQL connection closed safely")
            print("="*60 + "\n")

def verify_database():
    """
    Verify database setup by checking tables, functions, procedures, and triggers.
    """
    print("\n" + "="*60)
    print("🔍 Verifying Database Setup")
    print("="*60 + "\n")
    
    connection = None
    
    try:
        connection = get_db_connection()
        if not connection:
            return False
        
        db_name = os.getenv('MYSQL_DB', 'landwand')
        cursor = connection.cursor()
        cursor.execute(f"USE {db_name}")
        
        # Check tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"📋 Tables found: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")
        
        # Check stored procedures
        cursor.execute("SHOW PROCEDURE STATUS WHERE Db = %s", (db_name,))
        procedures = cursor.fetchall()
        print(f"\n⚙️  Stored Procedures: {len(procedures)}")
        for proc in procedures:
            print(f"   - {proc[1]}")
        
        # Check functions
        cursor.execute("SHOW FUNCTION STATUS WHERE Db = %s", (db_name,))
        functions = cursor.fetchall()
        print(f"\n🔧 Functions: {len(functions)}")
        for func in functions:
            print(f"   - {func[1]}")
        
        # Check triggers
        cursor.execute("SHOW TRIGGERS")
        triggers = cursor.fetchall()
        print(f"\n⚡ Triggers: {len(triggers)}")
        for trigger in triggers:
            print(f"   - {trigger[0]} on {trigger[2]}")
        
        cursor.close()
        print("\n✅ Verification complete!")
        return True
        
    except Error as e:
        print(f"❌ Error during verification: {e}")
        return False
        
    finally:
        if connection and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    # Check if .env file exists
    env_path = Path(__file__).parent.parent / 'backend' / '.env'
    if not env_path.exists():
        print("\n⚠️  Warning: .env file not found!")
        print(f"Please create {env_path} with your MySQL credentials.")
        print("\nExample:")
        print("MYSQL_HOST=localhost")
        print("MYSQL_USER=root")
        print("MYSQL_PASSWORD=your_password")
        print("MYSQL_DB=landwand\n")
    
    # Initialize database
    success = initialize_database()
    
    # Verify setup if initialization was successful
    if success:
        verify_database()
    else:
        print("\n⚠️  Database initialization failed. Please check the errors above.")
    
    # Exit with appropriate status code
    exit(0 if success else 1)
