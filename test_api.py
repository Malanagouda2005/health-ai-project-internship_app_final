"""
🏥 Health AI - Quick API Test Script
Test predictions without needing the frontend
"""

import requests
import json
from typing import List, Dict

# API Configuration
API_URL = 'http://localhost:5000'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{bcolors.HEADER}{bcolors.BOLD}{text}{bcolors.ENDC}")
    print("=" * 60)

def print_result(data: Dict, title: str = "Result"):
    """Pretty print API response"""
    print(f"\n{bcolors.OKGREEN}{title}{bcolors.ENDC}")
    print(json.dumps(data, indent=2))

def test_api_health():
    """Test if API is running"""
    print_header("🔌 Testing API Connection")
    
    try:
        response = requests.get(f'{API_URL}/api/status')
        if response.status_code == 200:
            print(f"{bcolors.OKGREEN}✅ API is running!{bcolors.ENDC}")
            return True
        else:
            print(f"{bcolors.FAIL}❌ API error: {response.status_code}{bcolors.ENDC}")
            return False
    except Exception as e:
        print(f"{bcolors.FAIL}❌ Cannot connect to API at {API_URL}{bcolors.ENDC}")
        print(f"   Error: {str(e)}")
        print(f"\n{bcolors.WARNING}Start backend with:{bcolors.ENDC}")
        print(f"   cd backend")
        print(f"   python app.py")
        return False

def test_symptom_prediction(symptoms: List[str]):
    """Test symptom prediction"""
    print_header(f"🤒 Testing Symptom Prediction")
    print(f"Symptoms: {', '.join(symptoms)}")
    
    try:
        response = requests.post(
            f'{API_URL}/api/predict/symptoms',
            json={'symptoms': symptoms},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                # Print detailed results
                print(f"\n{bcolors.OKGREEN}✅ Prediction successful!{bcolors.ENDC}")
                print(f"\n{bcolors.BOLD}Main Result:{bcolors.ENDC}")
                print(f"  Disease: {bcolors.OKCYAN}{result.get('predicted_disease')}{bcolors.ENDC}")
                print(f"  Confidence: {bcolors.OKBLUE}{result.get('confidence_percentage')}{bcolors.ENDC}")
                print(f"  Risk Level: {bcolors.WARNING}{result.get('risk_level')}{bcolors.ENDC}")
                print(f"  Risk Probability: {result.get('risk_probability')}")
                
                if result.get('medications'):
                    print(f"\n{bcolors.BOLD}Suggested Medications:{bcolors.ENDC}")
                    for med in result.get('medications', [])[:3]:
                        print(f"  • {med}")
                
                if result.get('treatments'):
                    print(f"\n{bcolors.BOLD}Treatments:{bcolors.ENDC}")
                    for treat in result.get('treatments', [])[:3]:
                        print(f"  • {treat}")
                
                if result.get('top_5_predictions'):
                    print(f"\n{bcolors.BOLD}Top Predictions:{bcolors.ENDC}")
                    for i, pred in enumerate(result.get('top_5_predictions', [])[:3], 1):
                        print(f"  {i}. {pred['disease']} ({pred['confidence_percentage']}) - {pred['risk_level']}")
                
                return True
            else:
                print(f"{bcolors.FAIL}❌ Prediction failed: {result.get('message')}{bcolors.ENDC}")
                return False
        else:
            print(f"{bcolors.FAIL}❌ API error: {response.status_code}{bcolors.ENDC}")
            print(response.text)
            return False
    except Exception as e:
        print(f"{bcolors.FAIL}❌ Error: {str(e)}{bcolors.ENDC}")
        return False

def test_disease_info(disease: str):
    """Get disease information"""
    print_header(f"ℹ️  Getting Disease Information")
    print(f"Disease: {disease}")
    
    try:
        response = requests.get(f'{API_URL}/api/disease/{disease}')
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n{bcolors.OKGREEN}✅ Disease info retrieved!{bcolors.ENDC}")
            details = result.get('details', {})
            print(f"\n{bcolors.BOLD}Details:{bcolors.ENDC}")
            print(f"  Description: {details.get('description')}")
            print(f"  Risk Level: {details.get('risk_level')}")
            print(f"  Duration: {details.get('recovery_duration')}")
            return True
        else:
            print(f"{bcolors.FAIL}❌ API error: {response.status_code}{bcolors.ENDC}")
            return False
    except Exception as e:
        print(f"{bcolors.FAIL}❌ Error: {str(e)}{bcolors.ENDC}")
        return False

def interactive_test():
    """Interactive testing mode"""
    print_header("🧪 Interactive Symptom Testing")
    
    available_symptoms = [
        'itching', 'skin_rash', 'continuous_sneezing', 'shivering', 'chills',
        'joint_pain', 'stomach_pain', 'acidity', 'muscle_wasting', 'vomiting',
        'fatigue', 'weight_gain', 'anxiety', 'cough', 'high_fever',
        'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache',
        'nausea', 'loss_of_appetite', 'back_pain', 'constipation', 'diarrhoea',
        'mild_fever', 'dizziness', 'cramps', 'chest_pain', 'weakness_in_limbs',
        'neck_pain', 'muscle_weakness', 'stiff_neck', 'depression', 'irritability',
        'muscle_pain', 'red_spots_over_body', 'watering_from_eyes'
    ]
    
    print("\n📝 Available symptoms (sample):")
    for i, sym in enumerate(available_symptoms[:20], 1):
        print(f"  {i:2}. {sym}")
    print(f"  ... and {len(available_symptoms) - 20} more")
    
    print(f"\n{bcolors.OKCYAN}Enter symptoms separated by commas (or 'demo' for example):{bcolors.ENDC}")
    user_input = input("➜ ").strip()
    
    if user_input.lower() == 'demo':
        # Demo: Cold symptoms
        symptoms = ['continuous_sneezing', 'high_fever', 'cough', 'headache']
        print(f"\n{bcolors.OKCYAN}Using demo symptoms: {', '.join(symptoms)}{bcolors.ENDC}")
    else:
        symptoms = [s.strip() for s in user_input.split(',')]
    
    # Run prediction
    if test_symptom_prediction(symptoms):
        # Also test disease info
        while True:
            more = input(f"\n{bcolors.OKBLUE}Get more info on a disease? (y/n): {bcolors.ENDC}").lower()
            if more == 'y':
                disease = input("Disease name (e.g., 'Pneumonia'): ").strip()
                test_disease_info(disease)
            else:
                break

def run_all_tests():
    """Run all predefined tests"""
    print(f"\n{bcolors.HEADER}{bcolors.BOLD}")
    print("╔════════════════════════════════════════╗")
    print("║  🏥 Health AI - API Test Suite        ║")
    print("╚════════════════════════════════════════╝")
    print(f"{bcolors.ENDC}")
    
    # Test 1: API Health
    if not test_api_health():
        return
    
    # Test 2: Cold/Flu Symptoms
    test_symptom_prediction([
        'continuous_sneezing',
        'high_fever',
        'cough',
        'congestion'
    ])
    
    # Test 3: Digestive Issues
    test_symptom_prediction([
        'stomach_pain',
        'acidity',
        'nausea',
        'loss_of_appetite'
    ])
    
    # Test 4: Pain/Fever
    test_symptom_prediction([
        'joint_pain',
        'mild_fever',
        'muscle_pain'
    ])
    
    # Test 5: Get disease info
    test_disease_info('Pneumonia')
    
    print(f"\n{bcolors.HEADER}{bcolors.BOLD}")
    print("✅ All tests completed!")
    print(f"{bcolors.ENDC}")

def main():
    """Main entry point"""
    import sys
    
    print(f"{bcolors.OKCYAN}")
    print("""
    ┌─────────────────────────────────────────┐
    │  🏥 Health AI - Quick Test              │
    └─────────────────────────────────────────┘
    
    Usage:
      python test_api.py          - Run all predefined tests
      python test_api.py i        - Interactive mode
      python test_api.py health   - Just check API health
    """)
    print(f"{bcolors.ENDC}")
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd == 'i' or cmd == 'interactive':
            if test_api_health():
                interactive_test()
        elif cmd == 'health':
            test_api_health()
        elif cmd == 'demo':
            if test_api_health():
                test_symptom_prediction([
                    'continuous_sneezing',
                    'high_fever',
                    'cough',
                    'headache'
                ])
        else:
            print(f"{bcolors.WARNING}Unknown command: {cmd}{bcolors.ENDC}")
            print("Use: 'i' (interactive), 'health', or 'demo'")
    else:
        # Default: run all tests
        run_all_tests()

if __name__ == '__main__':
    main()
