#!/usr/bin/env python3
"""
Master Training Script for Health AI Models
Trains and analyzes all models: Skin Disease, X-ray, and Symptom prediction
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🚀 {description}")
    print(f"Command: {command}")

    try:
        result = subprocess.run(command, shell=True, check=True,
                              capture_output=True, text=True)
        print("✅ Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def train_skin_model():
    """Train skin disease models"""
    print("\n" + "="*60)
    print("🩺 TRAINING SKIN DISEASE MODELS")
    print("="*60)

    # Check if data exists
    data_path = "data/datasets/SkinDisease/SkinDisease/train"
    if not os.path.exists(data_path):
        print(f"❌ Skin disease data not found at {data_path}")
        return False

    # Run training
    command = f"cd {os.getcwd()} && python model/skin_model.py"
    return run_command(command, "Training Skin Disease Models with EfficientNet & MobileNet")

def train_xray_model():
    """Train X-ray models"""
    print("\n" + "="*60)
    print("🫁 TRAINING X-RAY PNEUMONIA MODELS")
    print("="*60)

    # Check if data exists
    data_path = "data/datasets/chest_xray/train"
    if not os.path.exists(data_path):
        print(f"❌ X-ray data not found at {data_path}")
        return False

    # Run training
    command = f"cd {os.getcwd()} && python model/xray_model.py"
    return run_command(command, "Training X-ray Models with EfficientNet & MobileNet")

def train_symptom_model():
    """Train symptom prediction model"""
    print("\n" + "="*60)
    print("🤒 TRAINING SYMPTOM PREDICTION MODEL")
    print("="*60)

    # Check if data exists
    data_path = "data/raw/Training.csv"
    if not os.path.exists(data_path):
        print(f"❌ Symptom data not found at {data_path}")
        return False

    # Run training
    command = f"cd {os.getcwd()} && python backend/train_symptoms.py"
    return run_command(command, "Training Symptom Prediction Model with Multiple Algorithms")

def run_model_analysis():
    """Run comprehensive model analysis"""
    print("\n" + "="*60)
    print("📊 RUNNING COMPREHENSIVE MODEL ANALYSIS")
    print("="*60)

    command = f"cd {os.getcwd()} && python model/model_analysis.py"
    return run_command(command, "Analyzing All Trained Models")

def create_training_report():
    """Create a comprehensive training report"""
    print("\n" + "="*60)
    print("📋 GENERATING TRAINING REPORT")
    print("="*60)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        'training_session': timestamp,
        'models_trained': [],
        'performance_summary': {},
        'recommendations': []
    }

    # Check which models were trained
    models_status = {
        'skin_disease': False,
        'xray': False,
        'symptom': False
    }

    # Check for trained models
    for file in os.listdir('.'):
        if 'skin_model_' in file and file.endswith('.h5'):
            models_status['skin_disease'] = True
        if 'xray_model_' in file and file.endswith('.h5'):
            models_status['xray'] = True

    if os.path.exists('backend/symptom_model.pkl'):
        models_status['symptom'] = True

    # Load analysis results if available
    analysis_file = None
    for file in os.listdir('.'):
        if file.startswith('comprehensive_model_report_') and file.endswith('.json'):
            analysis_file = file
            break

    if analysis_file:
        try:
            with open(analysis_file, 'r') as f:
                analysis_data = json.load(f)
                report['performance_summary'] = analysis_data
        except:
            pass

    # Generate recommendations
    recommendations = []

    if models_status['skin_disease']:
        recommendations.append("✅ Skin disease models trained successfully")
        recommendations.append("   - Use EfficientNet for better accuracy")
        recommendations.append("   - Consider fine-tuning on more diverse skin images")
    else:
        recommendations.append("❌ Skin disease models not trained - check data availability")

    if models_status['xray']:
        recommendations.append("✅ X-ray models trained successfully")
        recommendations.append("   - Monitor AUC and recall for pneumonia detection")
        recommendations.append("   - Consider clinical validation before deployment")
    else:
        recommendations.append("❌ X-ray models not trained - check data availability")

    if models_status['symptom']:
        recommendations.append("✅ Symptom prediction model trained successfully")
        recommendations.append("   - Use RandomForest for reliable predictions")
        recommendations.append("   - Consider adding more symptom combinations")
    else:
        recommendations.append("❌ Symptom model not trained - check data availability")

    recommendations.extend([
        "",
        "🔧 General Recommendations:",
        "   - Implement model monitoring in production",
        "   - Consider ensemble methods for better accuracy",
        "   - Regular retraining with new data",
        "   - Validate models with domain experts"
    ])

    report['models_trained'] = [k for k, v in models_status.items() if v]
    report['recommendations'] = recommendations

    # Save report
    report_file = f'training_report_{timestamp}.json'
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)

    # Print summary
    print("\n📋 Training Session Summary:")
    print(f"Session ID: {timestamp}")
    print(f"Models Trained: {', '.join(report['models_trained']) if report['models_trained'] else 'None'}")

    print("\n📊 Performance Summary:")
    if report['performance_summary'].get('models'):
        for model_name, metrics in report['performance_summary']['models'].items():
            if 'accuracy' in metrics:
                print(".4f")

    print("\n💡 Recommendations:")
    for rec in recommendations:
        print(f"   {rec}")

    print(f"\n📁 Detailed report saved as: {report_file}")

    return report

def main():
    """Main training pipeline"""
    print("🏥 HEALTH AI MODEL TRAINING PIPELINE")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # Check requirements
    print("\n🔍 Checking Requirements...")

    # Check if required packages are available
    required_packages = ['tensorflow', 'pandas', 'scikit-learn', 'matplotlib', 'seaborn', 'imbalanced-learn']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + ' '.join(missing_packages))
        return

    # Run training pipeline
    training_results = {}

    # Train models
    training_results['skin'] = train_skin_model()
    training_results['xray'] = train_xray_model()
    training_results['symptom'] = train_symptom_model()

    # Run analysis
    training_results['analysis'] = run_model_analysis()

    # Create report
    report = create_training_report()

    # Final summary
    print("\n" + "="*60)
    print("🎉 TRAINING PIPELINE COMPLETED")
    print("="*60)

    successful = sum(training_results.values())
    total = len(training_results)

    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")

    if successful == total:
        print("\n🎊 All models trained successfully!")
        print("🚀 Ready for deployment and inference")
    else:
        print("\n⚠️ Some models failed to train. Check logs above.")

    print(f"\nFinished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()