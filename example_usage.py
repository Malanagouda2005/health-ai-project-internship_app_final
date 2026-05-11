#!/usr/bin/env python3
"""
Health AI System - Example Usage Script
Demonstrates how to use the system for predictions
"""

import os
import sys
import json
import numpy as np
from pathlib import Path

# Add backend to path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

def example_1_disease_database():
    """Example 1: Access disease information directly"""
    print("\n" + "="*80)
    print("EXAMPLE 1: DIRECT DISEASE DATABASE ACCESS")
    print("="*80)
    
    from disease_database import (
        get_disease_info, get_risk_level, get_medications,
        get_treatment_suggestions, get_diet_advice, get_activity_recommendations
    )
    
    diseases_to_check = ['Diabetes', 'Pneumonia', 'Acne', 'Asthma']
    
    for disease in diseases_to_check:
        print(f"\n📋 Disease: {disease}")
        print("-" * 80)
        
        info = get_disease_info(disease)
        if info:
            risk = get_risk_level(disease)
            meds = get_medications(disease)
            treatments = get_treatment_suggestions(disease)
            diet = get_diet_advice(disease)
            activities = get_activity_recommendations(disease)
            
            print(f"  Risk Level: {risk}")
            print(f"  Description: {info['description']}")
            print(f"  Medications: {meds[:2]} ({'...' if len(meds) > 2 else ''})")
            print(f"  Treatments: {treatments[:2]} ({'...' if len(treatments) > 2 else ''})")
            print(f"  Diet Advice: {diet[:2]} ({'...' if len(diet) > 2 else ''})")
            print(f"  Activities: {activities[:2]} ({'...' if len(activities) > 2 else ''})")
            print(f"  Recovery Time: {info['duration']}")
        else:
            print(f"  ❌ Disease not found in database")

def example_2_symptom_prediction():
    """Example 2: Symptom-based disease prediction"""
    print("\n" + "="*80)
    print("EXAMPLE 2: SYMPTOM-BASED DISEASE PREDICTION")
    print("="*80)
    
    try:
        import joblib
        
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        backend_path = os.path.join(backend_dir, 'backend')
        
        # Load model
        model_path = os.path.join(backend_path, 'symptom_model.pkl')
        encoder_path = os.path.join(backend_path, 'symptom_encoder.pkl')
        features_path = os.path.join(backend_path, 'symptom_features.pkl')
        
        if not os.path.exists(model_path):
            print("\n❌ Symptom model not trained. Run:")
            print("   python backend/train_symptoms_improved.py")
            return
        
        model = joblib.load(model_path)
        encoder = joblib.load(encoder_path)
        features = joblib.load(features_path)
        
        print(f"\n✓ Model loaded: {len(features)} features, {len(encoder.classes_)} diseases")
        
        # Test cases
        test_cases = [
            {
                "name": "Common Cold Symptoms",
                "symptoms": ["cough", "runny_nose", "sneezing", "sore_throat", "mild_fever"]
            },
            {
                "name": "Diabetes Symptoms",
                "symptoms": ["increased_thirst", "frequent_urination", "fatigue", "blurred_vision"]
            },
            {
                "name": "Asthma Symptoms",
                "symptoms": ["cough", "chest_tightness", "wheezing", "shortness_of_breath"]
            }
        ]
        
        for test_case in test_cases:
            print(f"\n📊 Test Case: {test_case['name']}")
            print(f"   Input Symptoms: {test_case['symptoms']}")
            print("-" * 80)
            
            # Create feature vector
            feature_vector = np.zeros(len(features))
            found_symptoms = []
            
            for symptom in test_case['symptoms']:
                if symptom in features:
                    idx = features.index(symptom)
                    feature_vector[idx] = 1
                    found_symptoms.append(symptom)
            
            if len(found_symptoms) == 0:
                print("   ⚠️  No symptoms found in feature list. Using random prediction for demo.")
                # Set random features for demonstration
                feature_vector[[0, 1, 2]] = 1
            
            # Make prediction
            probabilities = model.predict_proba([feature_vector])[0]
            top_indices = np.argsort(probabilities)[-5:][::-1]
            
            print(f"   Found Symptoms: {found_symptoms if found_symptoms else 'Demo data'}")
            print(f"\n   Top 5 Predictions:")
            
            for rank, idx in enumerate(top_indices, 1):
                disease = encoder.classes_[idx]
                confidence = probabilities[idx]
                
                # Get disease info
                from disease_database import get_risk_level
                risk = get_risk_level(disease)
                
                print(f"   {rank}. {disease:30} | Confidence: {confidence:6.2%} | Risk: {risk}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Make sure to train the symptom model first:")
        print("   python backend/train_symptoms_improved.py")

def example_3_api_requests():
    """Example 3: API requests using requests library"""
    print("\n" + "="*80)
    print("EXAMPLE 3: API REQUESTS (requires running backend)")
    print("="*80)
    
    try:
        import requests
    except ImportError:
        print("\n❌ 'requests' library not installed. Install with:")
        print("   pip install requests")
        return
    
    API_URL = "http://localhost:5000"
    
    print(f"\nNote: Make sure backend is running on {API_URL}")
    print("Run in another terminal: python backend/app_enhanced.py\n")
    
    try:
        # Test 1: Check API status
        print("1️⃣  Testing API Status...")
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            print(f"   ✓ API is running!")
            data = response.json()
            print(f"   Status: {data.get('status', 'unknown')}")
        else:
            print(f"   ❌ API not responding. Start it with:")
            print(f"      python backend/app_enhanced.py")
            return
        
        # Test 2: Get disease information
        print("\n2️⃣  Testing Disease Information Endpoint...")
        response = requests.get(f"{API_URL}/disease/Diabetes")
        if response.status_code == 200:
            data = response.json()
            disease_info = data['details']
            print(f"   ✓ Disease Info Retrieved!")
            print(f"   Disease: {data['disease']}")
            print(f"   Risk Level: {disease_info['risk_level']}")
            print(f"   Medications: {disease_info['medications'][:2]}")
            print(f"   Diet Advice: {disease_info['diet_advice'][:2]}")
        
        # Test 3: Symptom prediction
        print("\n3️⃣  Testing Symptom Prediction Endpoint...")
        symptoms = ["cough", "fever", "fatigue"]
        response = requests.post(
            f"{API_URL}/predict/symptoms",
            json={"symptoms": symptoms}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Prediction Successful!")
            print(f"   Input Symptoms: {symptoms}")
            print(f"   Predicted Disease: {data['predicted_disease']}")
            print(f"   Confidence: {data['confidence_percentage']}")
            print(f"   Risk Level: {data['risk_level']}")
            print(f"\n   Top 3 Predictions:")
            for i, pred in enumerate(data['top_5_predictions'][:3], 1):
                print(f"     {i}. {pred['disease']}: {pred['confidence_percentage']}")
            print(f"\n   Medications: {data['medications'][:2]}")
            print(f"   Diet Advice: {data['diet_advice'][:2]}")
            print(f"   Activities: {data['activity_recommendations'][:2]}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   {response.text}")
        
        # Test 4: Get cure recommendations
        print("\n4️⃣  Testing Cure Recommendations Endpoint...")
        response = requests.get(f"{API_URL}/cure/Pneumonia")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Cure Info Retrieved!")
            print(f"   Disease: {data['disease']}")
            print(f"   Risk Level: {data['risk_level']}")
            print(f"   Medications: {data['medications'][:2]}")
            print(f"   Treatments: {data['treatments'][:2]}")
        
        # Test 5: Check model status
        print("\n5️⃣  Testing Model Status Endpoint...")
        response = requests.get(f"{API_URL}/models/status")
        if response.status_code == 200:
            data = response.json()
            models = data['models']
            print(f"   ✓ Models Status:")
            for model_name, model_info in models.items():
                status = "✓" if model_info.get('loaded') else "✗"
                print(f"   {status} {model_name}: {model_info}")
    
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Could not connect to API at {API_URL}")
        print("Start the backend server with:")
        print("   python backend/app_enhanced.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

def example_4_complete_workflow():
    """Example 4: Complete workflow from symptoms to recommendations"""
    print("\n" + "="*80)
    print("EXAMPLE 4: COMPLETE WORKFLOW")
    print("="*80)
    
    from disease_database import (
        get_disease_info, get_risk_level, get_medications,
        get_treatment_suggestions, get_diet_advice, get_activity_recommendations
    )
    
    # Simulate a disease detection result
    detected_disease = "Diabetes"
    confidence_score = 0.89
    
    print(f"\n🔍 DISEASE DETECTED: {detected_disease}")
    print(f"📊 Confidence Score: {confidence_score:.2%}")
    print("="*80)
    
    # Get comprehensive information
    risk = get_risk_level(detected_disease)
    info = get_disease_info(detected_disease)
    
    print(f"\n⚠️  RISK LEVEL: {risk}")
    print(f"\n📋 DISEASE INFORMATION:")
    print(f"   {info['description']}")
    
    print(f"\n💊 MEDICATIONS:")
    for i, med in enumerate(info['medications'][:3], 1):
        print(f"   {i}. {med}")
    if len(info['medications']) > 3:
        print(f"   ... and {len(info['medications']) - 3} more")
    
    print(f"\n🏥 TREATMENTS:")
    for i, treatment in enumerate(info['treatments'][:3], 1):
        print(f"   {i}. {treatment}")
    if len(info['treatments']) > 3:
        print(f"   ... and {len(info['treatments']) - 3} more")
    
    print(f"\n🥗 DIET RECOMMENDATIONS:")
    for i, food in enumerate(info['diet_advice'][:3], 1):
        print(f"   {i}. {food}")
    if len(info['diet_advice']) > 3:
        print(f"   ... and {len(info['diet_advice']) - 3} more")
    
    print(f"\n🏃 RECOMMENDED ACTIVITIES:")
    for i, activity in enumerate(info['activities'][:3], 1):
        print(f"   {i}. {activity}")
    if len(info['activities']) > 3:
        print(f"   ... and {len(info['activities']) - 3} more")
    
    print(f"\n⏱️  RECOVERY DURATION:")
    print(f"   {info['duration']}")
    
    print(f"\n{'🚨 EMERGENCY ACTION REQUIRED!' if risk == 'High' else '✅ MANAGE WITH CARE AND MEDICAL SUPERVISION'}")

def main():
    """Main function to run all examples"""
    print("\n" + "="*80)
    print("🏥 HEALTH AI SYSTEM - USAGE EXAMPLES")
    print("="*80)
    
    examples = [
        ("1", "Disease Database Access", example_1_disease_database),
        ("2", "Symptom Prediction", example_2_symptom_prediction),
        ("3", "API Requests", example_3_api_requests),
        ("4", "Complete Workflow", example_4_complete_workflow),
    ]
    
    print("\nAvailable Examples:")
    for code, name, _ in examples:
        print(f"  {code}. {name}")
    print("  0. Run All Examples")
    print("  q. Quit")
    
    choice = input("\nEnter your choice (0-4, q): ").strip().lower()
    
    if choice == '0':
        for code, name, func in examples:
            print(f"\n\n{'*'*80}")
            print(f"Running Example {code}: {name}")
            print(f"{'*'*80}")
            try:
                func()
            except Exception as e:
                print(f"\n❌ Error in example: {str(e)}")
    elif choice == 'q':
        print("\nGoodbye! 👋\n")
        return
    else:
        for code, name, func in examples:
            if code == choice:
                try:
                    func()
                except Exception as e:
                    print(f"\n❌ Error: {str(e)}")
                break
    
    print(f"\n{'='*80}")
    print("✅ Examples completed!")
    print("\nFor more information:")
    print("  - See QUICK_START.md for quick reference")
    print("  - See ENHANCEMENT_GUIDE.md for detailed documentation")
    print(f"{'='*80}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user\n")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}\n")
