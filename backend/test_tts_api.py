#!/usr/bin/env python3
"""
Test script for Text-to-Speech API
This script tests all the TTS API endpoints
"""

import requests
import json
import time
import os
from typing import Dict, Any

class TTSAPITester:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, message: str = "", data: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "data": data,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        if data and success:
            print(f"   Data: {json.dumps(data, indent=2)}")
        print()
    
    def test_health_check(self):
        """Test basic health check endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Health Check", 
                    True, 
                    f"API is healthy - Status: {data.get('status')}", 
                    data
                )
                return True
            else:
                self.log_test(
                    "Health Check", 
                    False, 
                    f"Health check failed with status {response.status_code}"
                )
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_model_info(self):
        """Test TTS model info endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/tts/info", timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    model_info = data.get('data', {})
                    self.log_test(
                        "Model Info", 
                        True, 
                        f"Model loaded: {model_info.get('is_loaded')}", 
                        model_info
                    )
                    return True
                else:
                    self.log_test("Model Info", False, data.get('message', 'Unknown error'))
                    return False
            else:
                self.log_test("Model Info", False, f"HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Model Info", False, f"Request error: {str(e)}")
            return False
    
    def test_text_to_speech(self, text: str = "Hello world! This is a test message."):
        """Test text to speech conversion"""
        try:
            payload = {"text": text}
            response = requests.post(
                f"{self.base_url}/api/tts/convert", 
                json=payload, 
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    result_data = data.get('data', {})
                    filename = result_data.get('filename')
                    duration = result_data.get('duration_seconds')
                    
                    self.log_test(
                        "Text to Speech", 
                        True, 
                        f"Generated audio: {filename} ({duration:.2f}s)", 
                        result_data
                    )
                    return filename
                else:
                    self.log_test("Text to Speech", False, data.get('message', 'Unknown error'))
                    return None
            else:
                self.log_test("Text to Speech", False, f"HTTP {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.log_test("Text to Speech", False, f"Request error: {str(e)}")
            return None
    
    def test_download_audio(self, filename: str):
        """Test audio file download"""
        if not filename:
            self.log_test("Download Audio", False, "No filename provided")
            return False
        
        try:
            response = requests.get(
                f"{self.base_url}/api/tts/download/{filename}", 
                timeout=30
            )
            
            if response.status_code == 200:
                # Check if response is actually audio data
                content_type = response.headers.get('content-type', '')
                file_size = len(response.content)
                
                if 'audio' in content_type or filename.endswith('.wav'):
                    # Save file locally for testing
                    local_filename = f"test_{filename}"
                    with open(local_filename, 'wb') as f:
                        f.write(response.content)
                    
                    self.log_test(
                        "Download Audio", 
                        True, 
                        f"Downloaded {file_size} bytes to {local_filename}",
                        {"file_size": file_size, "content_type": content_type}
                    )
                    return True
                else:
                    self.log_test("Download Audio", False, f"Invalid content type: {content_type}")
                    return False
            else:
                self.log_test("Download Audio", False, f"HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Download Audio", False, f"Request error: {str(e)}")
            return False
    
    def test_invalid_requests(self):
        """Test API with invalid requests"""
        tests = [
            {
                "name": "Empty Text",
                "payload": {"text": ""},
                "expected_status": 400
            },
            {
                "name": "No Text Field",
                "payload": {"message": "hello"},
                "expected_status": 400
            },
            {
                "name": "Very Long Text",
                "payload": {"text": "a" * 10000},
                "expected_status": 500
            }
        ]
        
        for test in tests:
            try:
                response = requests.post(
                    f"{self.base_url}/api/tts/convert", 
                    json=test["payload"], 
                    timeout=30
                )
                
                success = response.status_code == test["expected_status"]
                self.log_test(
                    f"Invalid Request - {test['name']}", 
                    success, 
                    f"Expected {test['expected_status']}, got {response.status_code}"
                )
                
            except requests.exceptions.RequestException as e:
                self.log_test(
                    f"Invalid Request - {test['name']}", 
                    False, 
                    f"Request error: {str(e)}"
                )
    
    def test_cleanup(self):
        """Test file cleanup endpoint"""
        try:
            payload = {"max_age_hours": 0}  # Clean all files
            response = requests.post(
                f"{self.base_url}/api/tts/cleanup", 
                json=payload, 
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    cleanup_data = data.get('data', {})
                    deleted_count = cleanup_data.get('deleted_files', 0)
                    
                    self.log_test(
                        "File Cleanup", 
                        True, 
                        f"Deleted {deleted_count} files", 
                        cleanup_data
                    )
                    return True
                else:
                    self.log_test("File Cleanup", False, data.get('message', 'Unknown error'))
                    return False
            else:
                self.log_test("File Cleanup", False, f"HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("File Cleanup", False, f"Request error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting TTS API Tests")
        print("=" * 50)
        
        # Test basic connectivity
        if not self.test_health_check():
            print("❌ API is not accessible. Make sure the Flask server is running.")
            return
        
        # Test model loading
        self.test_model_info()
        
        # Test main functionality
        filename = self.test_text_to_speech()
        
        if filename:
            self.test_download_audio(filename)
        
        # Test edge cases
        self.test_invalid_requests()
        
        # Test cleanup
        self.test_cleanup()
        
        # Summary
        print("=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
        
        return failed_tests == 0

def main():
    """Main function to run tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test TTS API endpoints')
    parser.add_argument(
        '--url', 
        default='http://localhost:5000',
        help='Base URL of the API (default: http://localhost:5000)'
    )
    parser.add_argument(
        '--text',
        default='Hello world! This is a test message for text-to-speech conversion.',
        help='Text to convert to speech'
    )
    
    args = parser.parse_args()
    
    tester = TTSAPITester(args.url)
    
    print(f"Testing TTS API at: {args.url}")
    print(f"Test text: {args.text}")
    print()
    
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed!")
        exit(0)
    else:
        print("\n💥 Some tests failed!")
        exit(1)

if __name__ == "__main__":
    main()
