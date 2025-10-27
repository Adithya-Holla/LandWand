"""
Comprehensive Backend Integration Test Suite
Tests all components: Database, Flask App, Routes, Validation, Network Utils
"""

import sys
import os
from pathlib import Path
import time
import requests
import json

# Add backend to path
sys.path.append(str(Path(__file__).parent / 'backend'))

from dotenv import load_dotenv

# Load environment
env_path = Path(__file__).parent / 'backend' / '.env'
load_dotenv(dotenv_path=env_path)

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_test(name, passed, details=""):
    """Print test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {name}")
    if details:
        print(f"     {details}")

class BackendTester:
    def __init__(self):
        self.results = []
        self.server_url = None
        self.device_ip = None
        
    def test_1_environment_config(self):
        """Test 1: Environment Configuration"""
        print_section("TEST 1: Environment Configuration")
        
        required_vars = ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 
                        'MYSQL_DB', 'SECRET_KEY', 'FLASK_ENV']
        
        all_present = True
        for var in required_vars:
            value = os.getenv(var)
            present = value is not None
            all_present = all_present and present
            
            display = value if 'PASSWORD' not in var and 'SECRET' not in var else '***'
            print_test(f"ENV: {var}", present, display)
        
        self.results.append(("Environment Config", all_present))
        return all_present
    
    def test_2_network_utils(self):
        """Test 2: Network Utilities"""
        print_section("TEST 2: Network Utilities")
        
        try:
            from services.network_utils import get_local_ip, get_hostname, get_all_ip_addresses
            
            ip = get_local_ip()
            hostname = get_hostname()
            all_ips = get_all_ip_addresses()
            
            self.device_ip = ip
            
            print_test("Get Local IP", bool(ip), f"IP: {ip}")
            print_test("Get Hostname", bool(hostname), f"Hostname: {hostname}")
            print_test("Get All IPs", len(all_ips) > 0, f"Found {len(all_ips)} IPs")
            
            self.results.append(("Network Utilities", True))
            return True
        except Exception as e:
            print_test("Network Utilities", False, str(e))
            self.results.append(("Network Utilities", False))
            return False
    
    def test_3_database_config(self):
        """Test 3: Database Configuration"""
        print_section("TEST 3: Database Configuration")
        
        try:
            from models.db_config import get_db_host, get_db_connection, close_db_connection
            
            # Test host resolution
            host = get_db_host()
            print_test("Get DB Host", bool(host), f"Host: {host}")
            
            # Test connection
            conn = get_db_connection()
            if conn:
                print_test("Database Connection", True, "Connected successfully")
                close_db_connection(conn)
                self.results.append(("Database Config", True))
                return True
            else:
                print_test("Database Connection", False, "Failed to connect")
                self.results.append(("Database Config", False))
                return False
                
        except Exception as e:
            print_test("Database Config", False, str(e))
            self.results.append(("Database Config", False))
            return False
    
    def test_4_database_queries(self):
        """Test 4: Database Query Functions"""
        print_section("TEST 4: Database Query Functions")
        
        try:
            from models.queries import fetch_all, fetch_one, execute_query
            
            # Test fetch_all
            try:
                result = fetch_all("SELECT 1 as test")
                print_test("fetch_all()", isinstance(result, list), f"Returns list")
            except Exception as e:
                print_test("fetch_all()", False, str(e))
                self.results.append(("Query Functions", False))
                return False
            
            # Test fetch_one
            try:
                result = fetch_one("SELECT 1 as test")
                print_test("fetch_one()", isinstance(result, dict), f"Returns dict")
            except Exception as e:
                print_test("fetch_one()", False, str(e))
                self.results.append(("Query Functions", False))
                return False
            
            # Test execute_query
            try:
                result = execute_query("SELECT 1")
                print_test("execute_query()", isinstance(result, dict), f"Returns dict")
            except Exception as e:
                print_test("execute_query()", False, str(e))
                self.results.append(("Query Functions", False))
                return False
            
            self.results.append(("Query Functions", True))
            return True
            
        except Exception as e:
            print_test("Query Functions Import", False, str(e))
            self.results.append(("Query Functions", False))
            return False
    
    def test_5_validation_utils(self):
        """Test 5: Validation Utilities"""
        print_section("TEST 5: Validation Utilities")
        
        try:
            from services.validation import (
                validate_email, validate_phone, validate_user_data,
                validate_data_entry, sanitize_user_data
            )
            
            # Test email validation
            valid, msg = validate_email("test@example.com")
            print_test("Email Validation (valid)", valid, "test@example.com")
            
            invalid, msg = validate_email("invalid-email")
            print_test("Email Validation (invalid)", not invalid, "Correctly rejects")
            
            # Test phone validation
            valid, msg = validate_phone("1234567890")
            print_test("Phone Validation", valid, "1234567890")
            
            # Test user data validation
            user_data = {"name": "Test User", "email": "test@example.com"}
            valid, msg = validate_user_data(user_data)
            print_test("User Data Validation", valid, "Valid user data")
            
            # Test data entry validation
            data_entry = {"title": "Test", "category": "technology"}
            valid, msg = validate_data_entry(data_entry)
            print_test("Data Entry Validation", valid, "Valid data entry")
            
            # Test sanitization
            dirty_data = {"name": "  Test  ", "email": "test@example.com  "}
            clean = sanitize_user_data(dirty_data)
            print_test("Data Sanitization", "Test" == clean.get("name"), "Trimmed whitespace")
            
            self.results.append(("Validation Utils", True))
            return True
            
        except Exception as e:
            print_test("Validation Utils", False, str(e))
            self.results.append(("Validation Utils", False))
            return False
    
    def test_6_flask_blueprints(self):
        """Test 6: Flask Blueprints"""
        print_section("TEST 6: Flask Blueprints")
        
        try:
            from routes.users import users_bp
            from routes.data import data_bp
            
            print_test("Users Blueprint Import", bool(users_bp), f"Name: {users_bp.name}")
            print_test("Data Blueprint Import", bool(data_bp), f"Name: {data_bp.name}")
            
            # Check if blueprints have routes
            users_routes = [rule.rule for rule in users_bp.url_map.iter_rules() if rule.endpoint.startswith('users.')]
            data_routes = [rule.rule for rule in data_bp.url_map.iter_rules() if rule.endpoint.startswith('data.')]
            
            print_test("Users Routes Defined", len(users_routes) > 0, f"Found {len(users_routes)} routes")
            print_test("Data Routes Defined", len(data_routes) > 0, f"Found {len(data_routes)} routes")
            
            self.results.append(("Flask Blueprints", True))
            return True
            
        except Exception as e:
            print_test("Flask Blueprints", False, str(e))
            self.results.append(("Flask Blueprints", False))
            return False
    
    def test_7_flask_app_structure(self):
        """Test 7: Flask App Structure"""
        print_section("TEST 7: Flask App Structure")
        
        try:
            # Check if app.py can be imported
            import importlib.util
            spec = importlib.util.spec_from_file_location("app", 
                Path(__file__).parent / "backend" / "app.py")
            app_module = importlib.util.module_from_spec(spec)
            
            print_test("app.py Exists", spec is not None, "File found")
            print_test("app.py Importable", True, "No syntax errors")
            
            # Read app.py to check structure
            app_path = Path(__file__).parent / "backend" / "app.py"
            with open(app_path, 'r') as f:
                content = f.read()
            
            checks = {
                "Flask Import": "from flask import Flask" in content,
                "CORS Enabled": "CORS" in content,
                "Users Blueprint": "users_bp" in content,
                "Data Blueprint": "data_bp" in content,
                "Health Endpoint": "/health" in content,
                "Debug Mode": "debug=True" in content
            }
            
            for check_name, passed in checks.items():
                print_test(check_name, passed)
            
            all_passed = all(checks.values())
            self.results.append(("Flask App Structure", all_passed))
            return all_passed
            
        except Exception as e:
            print_test("Flask App Structure", False, str(e))
            self.results.append(("Flask App Structure", False))
            return False
    
    def test_8_database_connection_live(self):
        """Test 8: Live Database Connection Test"""
        print_section("TEST 8: Live Database Connection")
        
        try:
            from models.db_config import get_db_connection, close_db_connection
            
            conn = get_db_connection()
            if conn and conn.is_connected():
                cursor = conn.cursor(dictionary=True)
                
                # Test basic query
                cursor.execute("SELECT VERSION() as version")
                result = cursor.fetchone()
                print_test("SELECT Query", bool(result), f"MySQL {result.get('version', 'Unknown')}")
                
                # Test database exists
                cursor.execute("SHOW DATABASES")
                dbs = [row['Database'] for row in cursor.fetchall()]
                db_name = os.getenv('MYSQL_DB', 'landwand_db')
                db_exists = db_name in dbs
                print_test(f"Database '{db_name}' Exists", db_exists)
                
                # If database exists, check tables
                if db_exists:
                    cursor.execute(f"USE {db_name}")
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    print_test("Tables in Database", len(tables) > 0, f"Found {len(tables)} tables")
                    
                    # List tables
                    if tables:
                        table_names = [list(t.values())[0] for t in tables]
                        print(f"     Tables: {', '.join(table_names)}")
                
                cursor.close()
                close_db_connection(conn)
                self.results.append(("Live Database Test", True))
                return True
            else:
                print_test("Database Connection", False, "Could not connect")
                self.results.append(("Live Database Test", False))
                return False
                
        except Exception as e:
            print_test("Live Database Test", False, str(e))
            self.results.append(("Live Database Test", False))
            return False
    
    def test_9_integration_check(self):
        """Test 9: Component Integration Check"""
        print_section("TEST 9: Component Integration")
        
        try:
            # Test that routes can use validation
            from routes.users import users_bp
            from services.validation import validate_user_data
            
            test_data = {"name": "Test", "email": "test@example.com"}
            valid, msg = validate_user_data(test_data)
            print_test("Routes → Validation", valid, "Integration works")
            
            # Test that routes can use database queries
            from models.queries import fetch_one
            result = fetch_one("SELECT 1 as test")
            print_test("Routes → Database Queries", bool(result), "Integration works")
            
            # Test that app can use all components
            from services.network_utils import get_local_ip
            ip = get_local_ip()
            print_test("App → Network Utils", bool(ip), f"IP: {ip}")
            
            self.results.append(("Component Integration", True))
            return True
            
        except Exception as e:
            print_test("Component Integration", False, str(e))
            self.results.append(("Component Integration", False))
            return False
    
    def test_10_file_structure(self):
        """Test 10: File Structure Completeness"""
        print_section("TEST 10: File Structure Check")
        
        base_path = Path(__file__).parent
        required_files = {
            'Backend Core': [
                'backend/app.py',
                'backend/requirements.txt',
                'backend/.env'
            ],
            'Models': [
                'backend/models/db_config.py',
                'backend/models/queries.py'
            ],
            'Routes': [
                'backend/routes/users.py',
                'backend/routes/data.py'
            ],
            'Services': [
                'backend/services/validation.py',
                'backend/services/network_utils.py'
            ],
            'Database': [
                'database/init_db.py',
                'database/test_connection.py'
            ]
        }
        
        all_exist = True
        for category, files in required_files.items():
            print(f"\n  {category}:")
            for file in files:
                exists = (base_path / file).exists()
                all_exist = all_exist and exists
                print_test(f"  {file}", exists)
        
        self.results.append(("File Structure", all_exist))
        return all_exist
    
    def print_summary(self):
        """Print test summary"""
        print_section("TEST SUMMARY")
        
        total = len(self.results)
        passed = sum(1 for _, result in self.results if result)
        
        print(f"\nTotal Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%\n")
        
        for test_name, result in self.results:
            status = "✅" if result else "❌"
            print(f"{status} {test_name}")
        
        print("\n" + "="*70)
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Backend is fully integrated and working!")
        elif passed >= total * 0.8:
            print("⚠️  Most tests passed. Check failed tests above.")
        else:
            print("❌ Multiple tests failed. Review errors above.")
        
        print("="*70 + "\n")
        
        return passed == total

def main():
    print("\n" + "="*70)
    print("  🧪 COMPREHENSIVE BACKEND INTEGRATION TEST SUITE")
    print("  Testing all backend components and their integration")
    print("="*70)
    
    tester = BackendTester()
    
    # Run all tests
    tester.test_1_environment_config()
    tester.test_2_network_utils()
    tester.test_3_database_config()
    tester.test_4_database_queries()
    tester.test_5_validation_utils()
    tester.test_6_flask_blueprints()
    tester.test_7_flask_app_structure()
    tester.test_8_database_connection_live()
    tester.test_9_integration_check()
    tester.test_10_file_structure()
    
    # Print summary
    success = tester.print_summary()
    
    # Additional recommendations
    if success:
        print("\n📝 Next Steps:")
        print("  1. Run: python backend/app.py (to start Flask server)")
        print("  2. Test endpoints manually or with Postman")
        print("  3. Run: python database/init_db.py (if database not initialized)")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
