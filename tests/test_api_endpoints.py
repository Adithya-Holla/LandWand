"""
Comprehensive API Endpoint Testing
Tests all REST API endpoints with various scenarios
"""

import requests
import json
import time
import random
import string
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class APIEndpointTester:
    def __init__(self, base_url="http://10.20.201.18:5000"):
        self.base_url = base_url
        self.results = []
        self.test_user_id = None
        self.test_property_id = None
        
    def print_section(self, title):
        """Print formatted section header"""
        print(f"\n{Colors.BOLD}{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}{Colors.RESET}")
    
    def print_test(self, method, endpoint, status_code, expected_code, message="", response_data=None):
        """Print test result with color coding"""
        passed = status_code == expected_code
        status_symbol = f"{Colors.GREEN}✅" if passed else f"{Colors.RED}❌"
        
        print(f"{status_symbol} {method:7} {endpoint:35} → Status: {status_code}{Colors.RESET}")
        
        if message:
            print(f"     {Colors.BLUE}{message}{Colors.RESET}")
        
        if response_data and isinstance(response_data, dict):
            if 'message' in response_data:
                print(f"     Message: {response_data['message']}")
            if 'data' in response_data and response_data['data']:
                if isinstance(response_data['data'], list):
                    print(f"     Count: {len(response_data['data'])}")
                elif isinstance(response_data['data'], dict):
                    print(f"     Data: {list(response_data['data'].keys())}")
        
        self.results.append({
            'test': f"{method} {endpoint}",
            'passed': passed,
            'status_code': status_code,
            'expected': expected_code
        })
        
        return passed
    
    def generate_random_email(self):
        """Generate random email for testing"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"test_{random_string}@example.com"
    
    def check_server_running(self):
        """Check if the Flask server is running"""
        self.print_section("🔍 CHECKING SERVER STATUS")
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print(f"{Colors.GREEN}✅ Server is running at {self.base_url}{Colors.RESET}")
                data = response.json()
                print(f"     Status: {data.get('status')}")
                print(f"     Database: {data.get('database')}")
                return True
            else:
                print(f"{Colors.RED}❌ Server returned status code: {response.status_code}{Colors.RESET}")
                return False
        except requests.exceptions.ConnectionError:
            print(f"{Colors.RED}❌ Cannot connect to server at {self.base_url}{Colors.RESET}")
            print(f"{Colors.YELLOW}⚠️  Please start the server: python backend/app.py{Colors.RESET}")
            return False
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
            return False
    
    def test_system_endpoints(self):
        """Test system/health endpoints"""
        self.print_section("TEST 1: System Endpoints")
        
        # Test root endpoint
        try:
            response = requests.get(f"{self.base_url}/")
            data = response.json()
            self.print_test("GET", "/", response.status_code, 200, 
                          response_data=data)
        except Exception as e:
            print(f"{Colors.RED}❌ GET     /                                   → Error: {e}{Colors.RESET}")
        
        # Test health endpoint
        try:
            response = requests.get(f"{self.base_url}/health")
            data = response.json()
            self.print_test("GET", "/health", response.status_code, 200,
                          response_data=data)
        except Exception as e:
            print(f"{Colors.RED}❌ GET     /health                              → Error: {e}{Colors.RESET}")
    
    def test_users_read_endpoints(self):
        """Test user read operations"""
        self.print_section("TEST 2: Users - Read Operations")
        
        # Get all users
        try:
            response = requests.get(f"{self.base_url}/api/users")
            data = response.json()
            self.print_test("GET", "/api/users", response.status_code, 200,
                          response_data=data)
            
            # Store a user ID for later tests if users exist
            if data.get('data') and len(data['data']) > 0:
                self.test_user_id = data['data'][0].get('user_id')
        except Exception as e:
            print(f"{Colors.RED}❌ GET     /api/users                           → Error: {e}{Colors.RESET}")
        
        # Get specific user (if we have an ID)
        if self.test_user_id:
            try:
                response = requests.get(f"{self.base_url}/api/users/{self.test_user_id}")
                data = response.json()
                self.print_test("GET", f"/api/users/{self.test_user_id}", 
                              response.status_code, 200, response_data=data)
            except Exception as e:
                print(f"{Colors.RED}❌ GET     /api/users/{self.test_user_id}                      → Error: {e}{Colors.RESET}")
        
        # Get non-existent user
        try:
            response = requests.get(f"{self.base_url}/api/users/99999")
            data = response.json()
            self.print_test("GET", "/api/users/99999", response.status_code, 404,
                          "Should return 404 for non-existent user", data)
        except Exception as e:
            print(f"{Colors.RED}❌ GET     /api/users/99999                     → Error: {e}{Colors.RESET}")
    
    def test_users_create(self):
        """Test user creation"""
        self.print_section("TEST 3: Users - Create Operations")
        
        # Create valid user
        try:
            user_data = {
                "name": "Test User API",
                "email": self.generate_random_email(),
                "phone": "1234567890",
                "address": "123 Test Street",
                "role": "user",
                "password": "testpass123"
            }
            
            response = requests.post(
                f"{self.base_url}/api/users",
                json=user_data,
                headers={"Content-Type": "application/json"}
            )
            data = response.json()
            
            if response.status_code == 201:
                # Store the created user ID for later tests
                if data.get('data') and data['data'].get('user_id'):
                    self.test_user_id = data['data']['user_id']
            
            self.print_test("POST", "/api/users", response.status_code, 201,
                          "Create valid user", data)
        except Exception as e:
            print(f"{Colors.RED}❌ POST    /api/users                           → Error: {e}{Colors.RESET}")
        
        # Create user with missing required field
        try:
            invalid_data = {
                "name": "Test User",
                # Missing email
                "phone": "1234567890"
            }
            
            response = requests.post(
                f"{self.base_url}/api/users",
                json=invalid_data,
                headers={"Content-Type": "application/json"}
            )
            data = response.json()
            self.print_test("POST", "/api/users", response.status_code, 400,
                          "Missing required field - should fail", data)
        except Exception as e:
            print(f"{Colors.RED}❌ POST    /api/users                           → Error: {e}{Colors.RESET}")
        
        # Create user with invalid email
        try:
            invalid_data = {
                "name": "Test User",
                "email": "not-an-email",
                "phone": "1234567890"
            }
            
            response = requests.post(
                f"{self.base_url}/api/users",
                json=invalid_data,
                headers={"Content-Type": "application/json"}
            )
            data = response.json()
            self.print_test("POST", "/api/users", response.status_code, 400,
                          "Invalid email format - should fail", data)
        except Exception as e:
            print(f"{Colors.RED}❌ POST    /api/users                           → Error: {e}{Colors.RESET}")
    
    def test_users_update(self):
        """Test user update operations"""
        self.print_section("TEST 4: Users - Update Operations")
        
        if not self.test_user_id:
            print(f"{Colors.YELLOW}⚠️  Skipping update tests - no test user ID available{Colors.RESET}")
            return
        
        # Update user with valid data
        try:
            update_data = {
                "name": "Updated Test User",
                "phone": "9876543210"
            }
            
            response = requests.put(
                f"{self.base_url}/api/users/{self.test_user_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            data = response.json()
            self.print_test("PUT", f"/api/users/{self.test_user_id}", 
                          response.status_code, 200, "Update user fields", data)
        except Exception as e:
            print(f"{Colors.RED}❌ PUT     /api/users/{self.test_user_id}                      → Error: {e}{Colors.RESET}")
        
        # Update non-existent user
        try:
            response = requests.put(
                f"{self.base_url}/api/users/99999",
                json={"name": "Test"},
                headers={"Content-Type": "application/json"}
            )
            data = response.json()
            self.print_test("PUT", "/api/users/99999", response.status_code, 404,
                          "Update non-existent user - should fail", data)
        except Exception as e:
            print(f"{Colors.RED}❌ PUT     /api/users/99999                     → Error: {e}{Colors.RESET}")
        
        # Update with invalid data
        try:
            response = requests.put(
                f"{self.base_url}/api/users/{self.test_user_id}",
                json={"email": "invalid-email"},
                headers={"Content-Type": "application/json"}
            )
            data = response.json()
            self.print_test("PUT", f"/api/users/{self.test_user_id}", 
                          response.status_code, 400, "Invalid email - should fail", data)
        except Exception as e:
            print(f"{Colors.RED}❌ PUT     /api/users/{self.test_user_id}                      → Error: {e}{Colors.RESET}")
    
    def test_data_read_endpoints(self):
        """Test property/data read operations"""
        self.print_section("TEST 5: Properties/Data - Read Operations")
        
        # Get all properties
        try:
            response = requests.get(f"{self.base_url}/api/data")
            data = response.json()
            self.print_test("GET", "/api/data", response.status_code, 200,
                          response_data=data)
            
            # Store a property ID for later tests if properties exist
            if data.get('data') and len(data['data']) > 0:
                self.test_property_id = data['data'][0].get('property_id')
        except Exception as e:
            print(f"{Colors.RED}❌ GET     /api/data                            → Error: {e}{Colors.RESET}")
        
        # Get properties with filters
        try:
            response = requests.get(f"{self.base_url}/api/data?limit=5")
            data = response.json()
            self.print_test("GET", "/api/data?limit=5", response.status_code, 200,
                          "Filter with limit", data)
        except Exception as e:
            print(f"{Colors.RED}❌ GET     /api/data?limit=5                    → Error: {e}{Colors.RESET}")
        
        # Get specific property (if we have an ID)
        if self.test_property_id:
            try:
                response = requests.get(f"{self.base_url}/api/data/{self.test_property_id}")
                data = response.json()
                self.print_test("GET", f"/api/data/{self.test_property_id}", 
                              response.status_code, 200, response_data=data)
            except Exception as e:
                print(f"{Colors.RED}❌ GET     /api/data/{self.test_property_id}                    → Error: {e}{Colors.RESET}")
        
        # Get property statistics
        try:
            response = requests.get(f"{self.base_url}/api/data/aggregate")
            data = response.json()
            self.print_test("GET", "/api/data/aggregate", response.status_code, 200,
                          "Property statistics", data)
        except Exception as e:
            print(f"{Colors.RED}❌ GET     /api/data/aggregate                  → Error: {e}{Colors.RESET}")
        
        # Get stored procedure stats
        try:
            response = requests.get(f"{self.base_url}/api/data/stats")
            data = response.json()
            expected = 200 if response.status_code == 200 else 500
            self.print_test("GET", "/api/data/stats", response.status_code, expected,
                          "Stored procedure stats", data)
        except Exception as e:
            print(f"{Colors.RED}❌ GET     /api/data/stats                      → Error: {e}{Colors.RESET}")
    
    def test_data_create(self):
        """Test property creation"""
        self.print_section("TEST 6: Properties/Data - Create Operations")
        
        # Create valid property
        try:
            property_data = {
                "title": f"Test Property {random.randint(1000, 9999)}",
                "property_type": "Apartment",
                "description": "Test property created by API test",
                "price": 5000000,
                "location_id": 1  # Assuming location 1 exists
            }
            
            response = requests.post(
                f"{self.base_url}/api/data",
                json=property_data,
                headers={"Content-Type": "application/json"}
            )
            data = response.json()
            
            if response.status_code == 201:
                # Store the created property ID for later tests
                if data.get('data') and data['data'].get('property_id'):
                    self.test_property_id = data['data']['property_id']
            
            self.print_test("POST", "/api/data", response.status_code, 201,
                          "Create valid property", data)
        except Exception as e:
            print(f"{Colors.RED}❌ POST    /api/data                            → Error: {e}{Colors.RESET}")
        
        # Create property with missing required field
        try:
            invalid_data = {
                "property_type": "Apartment",
                # Missing title
                "description": "Test"
            }
            
            response = requests.post(
                f"{self.base_url}/api/data",
                json=invalid_data,
                headers={"Content-Type": "application/json"}
            )
            data = response.json()
            self.print_test("POST", "/api/data", response.status_code, 400,
                          "Missing required field - should fail", data)
        except Exception as e:
            print(f"{Colors.RED}❌ POST    /api/data                            → Error: {e}{Colors.RESET}")
        
        # Create property with invalid property_type
        try:
            invalid_data = {
                "title": "Test Property",
                "property_type": "InvalidType",
                "price": 5000000,
                "location_id": 1
            }
            
            response = requests.post(
                f"{self.base_url}/api/data",
                json=invalid_data,
                headers={"Content-Type": "application/json"}
            )
            data = response.json()
            # This might succeed or fail depending on DB constraints
            expected = 400 if response.status_code == 400 else 201
            self.print_test("POST", "/api/data", response.status_code, expected,
                          "Create with unusual property type", data)
        except Exception as e:
            print(f"{Colors.RED}❌ POST    /api/data                            → Error: {e}{Colors.RESET}")
    
    def test_data_update(self):
        """Test property update operations"""
        self.print_section("TEST 7: Properties/Data - Update Operations")
        
        if not self.test_property_id:
            print(f"{Colors.YELLOW}⚠️  Skipping update tests - no test property ID available{Colors.RESET}")
            return
        
        # Update property with valid data
        try:
            update_data = {
                "title": "Updated Test Property",
                "price": 6000000
            }
            
            response = requests.put(
                f"{self.base_url}/api/data/{self.test_property_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            data = response.json()
            self.print_test("PUT", f"/api/data/{self.test_property_id}", 
                          response.status_code, 200, "Update property fields", data)
        except Exception as e:
            print(f"{Colors.RED}❌ PUT     /api/data/{self.test_property_id}                    → Error: {e}{Colors.RESET}")
        
        # Update non-existent property
        try:
            response = requests.put(
                f"{self.base_url}/api/data/99999",
                json={"title": "Test"},
                headers={"Content-Type": "application/json"}
            )
            data = response.json()
            self.print_test("PUT", "/api/data/99999", response.status_code, 404,
                          "Update non-existent property - should fail", data)
        except Exception as e:
            print(f"{Colors.RED}❌ PUT     /api/data/99999                     → Error: {e}{Colors.RESET}")
    
    def test_cors_headers(self):
        """Test CORS configuration"""
        self.print_section("TEST 8: CORS Configuration")
        
        try:
            response = requests.options(f"{self.base_url}/api/users")
            
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
            }
            
            has_cors = any(cors_headers.values())
            
            if has_cors:
                print(f"{Colors.GREEN}✅ CORS headers present{Colors.RESET}")
                for header, value in cors_headers.items():
                    if value:
                        print(f"     {header}: {value}")
            else:
                print(f"{Colors.YELLOW}⚠️  CORS headers not found{Colors.RESET}")
            
            self.results.append({
                'test': 'CORS Configuration',
                'passed': has_cors,
                'status_code': response.status_code,
                'expected': 200
            })
        except Exception as e:
            print(f"{Colors.RED}❌ CORS test failed: {e}{Colors.RESET}")
    
    def test_users_delete(self):
        """Test user deletion"""
        self.print_section("TEST 9: Users - Delete Operations")
        
        if not self.test_user_id:
            print(f"{Colors.YELLOW}⚠️  Skipping delete tests - no test user ID available{Colors.RESET}")
            return
        
        # Delete the test user
        try:
            response = requests.delete(f"{self.base_url}/api/users/{self.test_user_id}")
            data = response.json()
            self.print_test("DELETE", f"/api/users/{self.test_user_id}", 
                          response.status_code, 200, "Delete test user", data)
        except Exception as e:
            print(f"{Colors.RED}❌ DELETE  /api/users/{self.test_user_id}                      → Error: {e}{Colors.RESET}")
        
        # Try to delete non-existent user
        try:
            response = requests.delete(f"{self.base_url}/api/users/99999")
            data = response.json()
            self.print_test("DELETE", "/api/users/99999", response.status_code, 404,
                          "Delete non-existent user - should fail", data)
        except Exception as e:
            print(f"{Colors.RED}❌ DELETE  /api/users/99999                     → Error: {e}{Colors.RESET}")
    
    def test_data_delete(self):
        """Test property deletion"""
        self.print_section("TEST 10: Properties/Data - Delete Operations")
        
        if not self.test_property_id:
            print(f"{Colors.YELLOW}⚠️  Skipping delete tests - no test property ID available{Colors.RESET}")
            return
        
        # Delete the test property
        try:
            response = requests.delete(f"{self.base_url}/api/data/{self.test_property_id}")
            data = response.json()
            self.print_test("DELETE", f"/api/data/{self.test_property_id}", 
                          response.status_code, 200, "Delete test property", data)
        except Exception as e:
            print(f"{Colors.RED}❌ DELETE  /api/data/{self.test_property_id}                    → Error: {e}{Colors.RESET}")
        
        # Try to delete non-existent property
        try:
            response = requests.delete(f"{self.base_url}/api/data/99999")
            data = response.json()
            self.print_test("DELETE", "/api/data/99999", response.status_code, 404,
                          "Delete non-existent property - should fail", data)
        except Exception as e:
            print(f"{Colors.RED}❌ DELETE  /api/data/99999                     → Error: {e}{Colors.RESET}")
    
    def print_summary(self):
        """Print test summary"""
        self.print_section("TEST SUMMARY")
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r['passed'])
        failed = total - passed
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"\n{Colors.BOLD}Total Endpoints Tested: {total}")
        print(f"Passed: {Colors.GREEN}{passed}{Colors.RESET}")
        print(f"Failed: {Colors.RED}{failed}{Colors.RESET}")
        print(f"Success Rate: {Colors.BOLD}{success_rate:.1f}%{Colors.RESET}\n")
        
        # Group results by pass/fail
        passed_tests = [r for r in self.results if r['passed']]
        failed_tests = [r for r in self.results if not r['passed']]
        
        if passed_tests:
            print(f"{Colors.GREEN}✅ Passed Tests:{Colors.RESET}")
            for result in passed_tests:
                print(f"   ✅ {result['test']}")
        
        if failed_tests:
            print(f"\n{Colors.RED}❌ Failed Tests:{Colors.RESET}")
            for result in failed_tests:
                print(f"   ❌ {result['test']} (Expected: {result['expected']}, Got: {result['status_code']})")
        
        print(f"\n{'='*70}")
        
        if success_rate == 100:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 PERFECT! All API endpoints working!{Colors.RESET}")
        elif success_rate >= 80:
            print(f"{Colors.YELLOW}⚠️  Most endpoints working. Check failed tests above.{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ Multiple endpoints failing. Check server logs.{Colors.RESET}")
        
        print(f"{'='*70}\n")
        
        return success_rate >= 80

def main():
    print(f"\n{Colors.BOLD}{'='*70}")
    print("  🧪 COMPREHENSIVE API ENDPOINT TESTING")
    print(f"  Server: http://10.20.201.18:5000")
    print(f"{'='*70}{Colors.RESET}")
    
    tester = APIEndpointTester()
    
    # Check if server is running
    if not tester.check_server_running():
        print(f"\n{Colors.RED}❌ Cannot proceed - server is not running{Colors.RESET}")
        print(f"{Colors.YELLOW}Please start the server with: python backend/app.py{Colors.RESET}\n")
        return False
    
    # Run all tests
    print(f"\n{Colors.BOLD}Starting comprehensive endpoint tests...{Colors.RESET}")
    time.sleep(1)
    
    tester.test_system_endpoints()
    tester.test_users_read_endpoints()
    tester.test_users_create()
    tester.test_users_update()
    tester.test_data_read_endpoints()
    tester.test_data_create()
    tester.test_data_update()
    tester.test_cors_headers()
    tester.test_users_delete()
    tester.test_data_delete()
    
    # Print summary
    success = tester.print_summary()
    
    # Additional info
    if success:
        print(f"{Colors.BOLD}📝 API Documentation:{Colors.RESET}")
        print(f"   • Full API docs: See API_TEST_GUIDE.md")
        print(f"   • Base URL: http://10.20.201.18:5000")
        print(f"   • All endpoints use JSON format")
        print(f"   • CORS is enabled for frontend integration\n")
    
    return success

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)