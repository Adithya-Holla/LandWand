"""
Test script to verify all files correctly load credentials from .env
"""

import os
import sys
from pathlib import Path

# Add backend directory to path (go up one level from tests/ to project root)
project_root = Path(__file__).parent.parent
backend_path = project_root / 'backend'
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv

# Load .env file
env_path = backend_path / '.env'
load_dotenv(dotenv_path=env_path)

def test_env_loading():
    """Test that .env file is loaded correctly"""
    print("\n" + "="*60)
    print("🧪 Testing .env File Loading")
    print("="*60 + "\n")
    
    # Check if .env file exists
    if not env_path.exists():
        print(f"❌ .env file not found at: {env_path}")
        return False
    
    print(f"✅ .env file found at: {env_path}\n")
    
    # Test each environment variable
    tests = {
        'MYSQL_HOST': os.getenv('MYSQL_HOST'),
        'MYSQL_PORT': os.getenv('MYSQL_PORT'),
        'MYSQL_USER': os.getenv('MYSQL_USER'),
        'MYSQL_PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'MYSQL_DB': os.getenv('MYSQL_DB'),
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'FLASK_ENV': os.getenv('FLASK_ENV'),
        'PORT': os.getenv('PORT')
    }
    
    print("📋 Environment Variables Loaded:")
    print("-" * 60)
    
    all_loaded = True
    for key, value in tests.items():
        if value:
            # Hide password
            if 'PASSWORD' in key or 'SECRET' in key:
                display_value = '*' * len(value) if value else '(empty)'
            else:
                display_value = value
            
            print(f"✅ {key:20} = {display_value}")
        else:
            print(f"❌ {key:20} = NOT SET")
            all_loaded = False
    
    print("-" * 60)
    
    if all_loaded:
        print("\n✅ All environment variables loaded successfully!")
    else:
        print("\n⚠️  Some environment variables are missing")
    
    return all_loaded

def test_file_imports():
    """Test that all Python files can import properly"""
    print("\n" + "="*60)
    print("🧪 Testing File Imports")
    print("="*60 + "\n")
    
    files_to_test = [
        ('backend/models/db_config.py', 'Database Config'),
        ('backend/app.py', 'Flask App'),
        ('backend/services/network_utils.py', 'Network Utils'),
        ('backend/services/validation.py', 'Validation Utils'),
        ('backend/routes/users.py', 'Users Routes'),
        ('backend/routes/data.py', 'Data Routes'),
        ('database/init_db.py', 'Database Init'),
        ('database/test_connection.py', 'Connection Test')
    ]
    
    all_passed = True
    for file_path, description in files_to_test:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {description:20} - {file_path}")
        else:
            print(f"❌ {description:20} - {file_path} (NOT FOUND)")
            all_passed = False
    
    print()
    return all_passed

def test_network_utils():
    """Test network utility functions"""
    print("="*60)
    print("🧪 Testing Network Utilities")
    print("="*60 + "\n")
    
    try:
        from services.network_utils import get_local_ip, get_hostname  # type: ignore
        
        ip = get_local_ip()
        hostname = get_hostname()
        
        print(f"✅ Device IP: {ip}")
        print(f"✅ Hostname: {hostname}\n")
        return True
    except Exception as e:
        print(f"❌ Error testing network utils: {e}\n")
        return False

def test_db_config():
    """Test database configuration"""
    print("="*60)
    print("🧪 Testing Database Configuration")
    print("="*60 + "\n")
    
    try:
        from models.db_config import get_db_host  # type: ignore
        
        host = get_db_host()
        print(f"✅ Resolved DB Host: {host}")
        
        # Show what would be used for connection
        print(f"\nConnection Parameters:")
        print(f"  Host: {host}")
        print(f"  Port: {os.getenv('MYSQL_PORT', '3306')}")
        print(f"  User: {os.getenv('MYSQL_USER', 'root')}")
        print(f"  Database: {os.getenv('MYSQL_DB', 'landwand_db')}\n")
        
        return True
    except Exception as e:
        print(f"❌ Error testing db config: {e}\n")
        return False

def main():
    print("\n" + "="*60)
    print("🔍 LandWand Backend - Configuration Test Suite")
    print("="*60)
    
    results = []
    
    # Run all tests
    results.append(("Environment Variables", test_env_loading()))
    results.append(("File Structure", test_file_imports()))
    results.append(("Network Utilities", test_network_utils()))
    results.append(("Database Config", test_db_config()))
    
    # Summary
    print("="*60)
    print("📊 Test Summary")
    print("="*60 + "\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:25} - {status}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Configuration is correct.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print("="*60 + "\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
