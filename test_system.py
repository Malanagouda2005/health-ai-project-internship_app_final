"""
🏥 Health AI System - Validation & Testing Script
This script validates that everything is set up correctly and working.
"""

import requests
import json
import time
import os
import sys
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(title):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.RESET}\n")

def print_success(msg):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")

def print_error(msg):
    """Print error message"""
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def print_warning(msg):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.RESET}")

def print_info(msg):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ️  {msg}{Colors.RESET}")

def check_file_exists(file_path, description):
    """Check if a required file exists"""
    if os.path.exists(file_path):
        print_success(f"{description} exists")
        return True
    else:
        print_error(f"{description} NOT FOUND: {file_path}")
        return False

def check_api_connection(url):
    """Check if API is running"""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def test_symptom_prediction():
    """Test symptom prediction API"""
    try:
        print_info("Testing symptom prediction...")
        
        test_data = {
            "symptoms": ["headache", "high_fever", "cough"]
        }
        
        response = requests.post(
            'http://localhost:5000/api/predict/symptoms',
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                print_success("Symptom prediction works!")
                print_info(f"  Disease: {result.get('predicted_disease')}")
                print_info(f"  Confidence: {result.get('confidence_percentage')}")
                print_info(f"  Risk Level: {result.get('risk_level')}")
                return True
            else:
                print_warning(f"API returned error: {result.get('message')}")
                return False
        else:
            print_error(f"API returned status {response.status_code}")
            print_info(f"Response: {response.text[:200]}")
            return False
    except Exception as e:
        print_error(f"Symptom prediction failed: {str(e)}")
        return False

def main():
    """Run all validation checks"""
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔════════════════════════════════════════╗")
    print("║  🏥 Health AI Validation & Test Suite  ║")
    print("╚════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    
    # Get base directory
    base_dir = Path(__file__).parent.absolute()
    print_info(f"Working directory: {base_dir}")
    
    passed = 0
    failed = 0
    
    # ==================== Check Required Files ====================
    print_header("📁 Checking Required Files")
    
    files_to_check = [
        ('backend/app.py', 'Backend Flask App'),
        ('backend/symptom_model.pkl', 'Symptom Model'),
        ('backend/symptom_encoder.pkl', 'Symptom Encoder'),
        ('backend/symptom_features.pkl', 'Symptom Features'),
        ('backend/disease_database.py', 'Disease Database'),
        ('frontend/src/components/HealthForm.js', 'Frontend HealthForm'),
        ('skin_model.h5', 'Skin Disease Model'),
        ('xray_model.h5', 'X-Ray Model'),
    ]
    
    for file_path, description in files_to_check:
        full_path = base_dir / file_path
        if check_file_exists(full_path, description):
            passed += 1
        else:
            failed += 1
    
    # ==================== Check API Connection ====================
    print_header("🔌 Checking API Connection")
    
    print_info("Checking if backend is running on http://localhost:5000...")
    
    if check_api_connection('http://localhost:5000/api/status'):
        print_success("Backend is running!")
        passed += 1
        
        # Get model status
        try:
            response = requests.get('http://localhost:5000/api/status')
            if response.status_code == 200:
                status = response.json()
                print_info("Model Status:")
                
                models = status.get('models', {})
                
                if models.get('skin_disease_model', {}).get('loaded'):
                    print_success("  Skin Disease Model loaded")
                else:
                    print_warning("  Skin Disease Model not loaded")
                
                if models.get('xray_model', {}).get('loaded'):
                    print_success("  X-Ray Model loaded")
                else:
                    print_warning("  X-Ray Model not loaded")
                
                if models.get('symptom_model', {}).get('loaded'):
                    print_success("  Symptom Model loaded")
                    features = models.get('symptom_model', {}).get('features', 0)
                    diseases = models.get('symptom_model', {}).get('diseases', 0)
                    print_info(f"    Features: {features}, Diseases: {diseases}")
                else:
                    print_error("  Symptom Model NOT loaded")
                    failed += 1
                
                if models.get('disease_database', {}).get('loaded'):
                    print_success("  Disease Database loaded")
                else:
                    print_warning("  Disease Database not loaded")
        except Exception as e:
            print_error(f"Failed to get model status: {str(e)}")
    else:
        print_error("Backend is NOT running at http://localhost:5000")
        print_info("Start the backend with: cd backend && python app.py")
        failed += 1
        return  # Can't continue without backend
    
    # ==================== Test API Endpoints ====================
    print_header("🧪 Testing API Endpoints")
    
    # Test health check
    print_info("Testing /api/status endpoint...")
    if check_api_connection('http://localhost:5000/api/status'):
        print_success("Health check endpoint works")
        passed += 1
    else:
        print_error("Health check endpoint failed")
        failed += 1
    
    # Test symptom prediction
    print_info("Testing /api/predict/symptoms endpoint...")
    if test_symptom_prediction():
        passed += 1
    else:
        failed += 1
    
    # ==================== Check Frontend ====================
    print_header("🌐 Checking Frontend")
    
    frontend_files = [
        'frontend/package.json',
        'frontend/public/index.html',
        'frontend/src/App.js',
    ]
    
    for file_path in frontend_files:
        full_path = base_dir / file_path
        if check_file_exists(full_path, file_path.split('/')[-1]):
            passed += 1
        else:
            failed += 1
    
    # ==================== Summary ====================
    print_header("📊 Test Summary")
    
    total = passed + failed
    percentage = (passed / total * 100) if total > 0 else 0
    
    print_info(f"Passed: {Colors.GREEN}{passed}{Colors.RESET}")
    print_info(f"Failed: {Colors.RED}{failed}{Colors.RESET}")
    print_info(f"Total:  {total}")
    print_info(f"Success Rate: {percentage:.1f}%")
    
    print()
    if failed == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ ALL CHECKS PASSED! System is ready!{Colors.RESET}")
        print_info("You can now:")
        print_info("  1. Open http://localhost:3000 in your browser")
        print_info("  2. Go to 'Symptoms' tab")
        print_info("  3. Select symptoms and click 'Predict'")
        print_info("  4. View results in 'Results' tab")
    else:
        print(f"{Colors.RED}{Colors.BOLD}⚠️  Some checks failed. Please review above.{Colors.RESET}")
        print_warning("Common issues:")
        print_warning("  1. Backend not running - start with: cd backend && python app.py")
        print_warning("  2. Models not trained - run: python backend/train_symptoms_improved.py")
        print_warning("  3. Missing files - ensure all files are in correct locations")
    
    print()
    print(f"{Colors.CYAN}For more help, see: PRODUCTION_FIX_GUIDE.md{Colors.RESET}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Test interrupted by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {str(e)}{Colors.RESET}")
        sys.exit(1)
