#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Medcures
Tests all API endpoints, authentication, chat functionality, and integrations
"""

import requests
import sys
import json
from datetime import datetime
import time

class MedcuresAPITester:
    def __init__(self, base_url="https://pharmabot-ai."):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_data = None
        self.tests_run = 0
        self.tests_passed = 0
        self.session_id = None
        
        # Test user credentials
        self.test_email = "test@medcures.com"
        self.test_password = "test123"
        self.test_name = "Test User"

    def log_test(self, name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        if details:
            print(f"   Details: {details}")

    def make_request(self, method, endpoint, data=None, expected_status=200, auth_required=False):
        """Make HTTP request with proper error handling"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if auth_required and self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)
            
            success = response.status_code == expected_status
            response_data = {}
            
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text}
            
            return success, response.status_code, response_data
            
        except requests.exceptions.Timeout:
            return False, 0, {"error": "Request timeout"}
        except requests.exceptions.ConnectionError:
            return False, 0, {"error": "Connection error"}
        except Exception as e:
            return False, 0, {"error": str(e)}

    def test_root_endpoint(self):
        """Test API root endpoint"""
        success, status, data = self.make_request('GET', '', expected_status=200)
        self.log_test("API Root Endpoint", success, 
                     f"Status: {status}, Response: {data}")
        return success

    def test_signup(self):
        """Test user signup"""
        # Use timestamp to ensure unique email
        timestamp = int(time.time())
        signup_data = {
            "email": f"testuser_{timestamp}@medcures.com",
            "password": self.test_password,
            "name": f"Test User {timestamp}"
        }
        
        success, status, data = self.make_request('POST', 'auth/signup', signup_data, 200)
        
        if success and 'token' in data:
            self.token = data['token']
            self.user_data = data['user']
            self.log_test("User Signup", True, f"User created: {data['user']['email']}")
        else:
            self.log_test("User Signup", False, f"Status: {status}, Data: {data}")
        
        return success

    def test_login(self):
        """Test user login with existing credentials"""
        login_data = {
            "email": self.test_email,
            "password": self.test_password
        }
        
        success, status, data = self.make_request('POST', 'auth/login', login_data, 200)
        
        if success and 'token' in data:
            self.token = data['token']
            self.user_data = data['user']
            self.log_test("User Login", True, f"Logged in: {data['user']['email']}")
        else:
            self.log_test("User Login", False, f"Status: {status}, Data: {data}")
        
        return success

    def test_auth_me(self):
        """Test /auth/me endpoint"""
        if not self.token:
            self.log_test("Auth Me", False, "No token available")
            return False
        
        success, status, data = self.make_request('GET', 'auth/me', auth_required=True)
        
        if success and 'email' in data:
            self.log_test("Auth Me", True, f"User info retrieved: {data['email']}")
        else:
            self.log_test("Auth Me", False, f"Status: {status}, Data: {data}")
        
        return success

    def test_chat_aspirin(self):
        """Test chat with Aspirin query (should find drug info)"""
        chat_data = {
            "message": "Tell me about Aspirin",
            "session_id": None
        }
        
        success, status, data = self.make_request('POST', 'chat/send', chat_data, 200)
        
        if success:
            self.session_id = data.get('session_id')
            has_response = bool(data.get('response'))
            has_citations = bool(data.get('citations'))
            has_drug_info = bool(data.get('drug_info'))
            
            details = f"Response: {len(data.get('response', ''))} chars, Citations: {has_citations}, Drug Info: {has_drug_info}"
            self.log_test("Chat - Aspirin Query", has_response, details)
            
            # Check if response contains disclaimer
            response_text = data.get('response', '')
            has_disclaimer = '⚠️' in response_text or 'educational purposes' in response_text.lower()
            self.log_test("Chat - Disclaimer Present", has_disclaimer, 
                         f"Disclaimer found: {has_disclaimer}")
            
            return has_response
        else:
            self.log_test("Chat - Aspirin Query", False, f"Status: {status}, Data: {data}")
            return False

    def test_chat_unknown_drug(self):
        """Test chat with unknown drug (should return out of context)"""
        chat_data = {
            "message": "Tell me about Morphine",
            "session_id": self.session_id
        }
        
        success, status, data = self.make_request('POST', 'chat/send', chat_data, 200)
        
        if success:
            response_text = data.get('response', '').lower()
            is_out_of_context = 'out of my context' in response_text or 'out of context' in response_text
            
            self.log_test("Chat - Unknown Drug (Out of Context)", is_out_of_context,
                         f"Response indicates out of context: {is_out_of_context}")
            return is_out_of_context
        else:
            self.log_test("Chat - Unknown Drug", False, f"Status: {status}, Data: {data}")
            return False

    def test_chat_paracetamol(self):
        """Test chat with Paracetamol query"""
        chat_data = {
            "message": "What is Paracetamol used for?",
            "session_id": self.session_id
        }
        
        success, status, data = self.make_request('POST', 'chat/send', chat_data, 200)
        
        if success:
            has_response = bool(data.get('response'))
            has_drug_info = bool(data.get('drug_info'))
            
            details = f"Response length: {len(data.get('response', ''))}, Drug info: {has_drug_info}"
            self.log_test("Chat - Paracetamol Query", has_response, details)
            return has_response
        else:
            self.log_test("Chat - Paracetamol Query", False, f"Status: {status}, Data: {data}")
            return False

    def test_feedback_submit(self):
        """Test feedback submission"""
        if not self.session_id:
            self.log_test("Feedback Submit", False, "No session ID available")
            return False
        
        feedback_data = {
            "session_id": self.session_id,
            "message_id": f"{self.session_id}-1",
            "rating": "positive",
            "message_content": "Tell me about Aspirin",
            "response_content": "Aspirin is a medication..."
        }
        
        success, status, data = self.make_request('POST', 'feedback/submit', feedback_data, 200)
        
        if success:
            self.log_test("Feedback Submit", True, f"Feedback submitted successfully")
        else:
            self.log_test("Feedback Submit", False, f"Status: {status}, Data: {data}")
        
        return success

    def test_chat_history(self):
        """Test chat history retrieval"""
        if not self.session_id:
            self.log_test("Chat History", False, "No session ID available")
            return False
        
        success, status, data = self.make_request('GET', f'chat/history/{self.session_id}')
        
        if success and isinstance(data, list):
            self.log_test("Chat History", True, f"Retrieved {len(data)} messages")
        else:
            self.log_test("Chat History", False, f"Status: {status}, Data: {data}")
        
        return success

    def test_invalid_auth(self):
        """Test invalid authentication"""
        # Save current token
        original_token = self.token
        self.token = "invalid_token_12345"
        
        success, status, data = self.make_request('GET', 'auth/me', auth_required=True, expected_status=401)
        
        # Restore original token
        self.token = original_token
        
        self.log_test("Invalid Auth Handling", success, f"Correctly rejected invalid token")
        return success

    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 Starting Medcures Backend API Tests")
        print(f"📍 Testing against: {self.base_url}")
        print("=" * 60)
        
        # Basic connectivity
        self.test_root_endpoint()
        
        # Authentication tests
        auth_success = self.test_signup()
        if not auth_success:
            # Try login if signup fails
            auth_success = self.test_login()
        
        if auth_success:
            self.test_auth_me()
        
        # Chat functionality tests
        self.test_chat_aspirin()
        self.test_chat_unknown_drug()
        self.test_chat_paracetamol()
        
        # Additional features
        self.test_feedback_submit()
        self.test_chat_history()
        
        # Security tests
        self.test_invalid_auth()
        
        # Results summary
        print("\n" + "=" * 60)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 Backend tests mostly successful!")
            return 0
        elif success_rate >= 60:
            print("⚠️  Backend has some issues but core functionality works")
            return 1
        else:
            print("❌ Backend has significant issues")
            return 2

def main():
    """Main test execution"""
    tester = MedcuresAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())