import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def analyze_all_models():
    """Comprehensive analysis of all trained models"""
    print("🔍 Comprehensive Model Analysis Report")
    print("=" * 50)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        'timestamp': timestamp,
        'models': {}
    }

    # 1. Analyze Symptom Model
    print("\n📊 Analyzing Symptom Prediction Model...")
    try:
        with open('backend/symptom_training_results.json', 'r') as f:
            symptom_results = json.load(f)

        report['models']['symptom'] = symptom_results
        print("✅ Symptom model results loaded")
        print(f"   Best Model: {symptom_results['best_model']}")
        print(".4f")
        print(f"   Cross-validation: {symptom_results['cv_mean']:.4f} ± {symptom_results['cv_std']:.4f}")
        print(f"   Classes: {symptom_results['n_classes']}")
        print(f"   Features: {symptom_results['n_features_selected']}")

    except FileNotFoundError:
        print("❌ Symptom model results not found. Run train_symptoms.py first.")

    # 2. Analyze Skin Disease Models
    print("\n📊 Analyzing Skin Disease Models...")
    skin_models = {}
    for file in os.listdir('.'):
        if file.startswith(('efficientnet_skin_model_', 'mobilenet_skin_model_')) and file.endswith('.h5'):
            model_name = file.split('_')[0]
            skin_models[model_name] = file

    if skin_models:
        # Load class names
        try:
            with open('skin_class_names.json', 'r') as f:
                class_names = json.load(f)
        except:
            class_names = [f'class_{i}' for i in range(22)]  # Default for skin diseases

        # Load test data
        test_datagen = ImageDataGenerator(rescale=1./255)
        test_generator = test_datagen.flow_from_directory(
            'data/datasets/SkinDisease/SkinDisease/test',
            target_size=(224, 224),
            batch_size=32,
            class_mode='categorical',
            shuffle=False
        )

        for model_name, model_file in skin_models.items():
            print(f"   Analyzing {model_name}...")
            try:
                model = tf.keras.models.load_model(model_file)
                results = model.evaluate(test_generator, verbose=0)

                # Get predictions
                predictions = model.predict(test_generator, verbose=0)
                y_true = test_generator.classes
                y_pred = np.argmax(predictions, axis=1)

                # Calculate metrics
                accuracy = results[1] if len(results) > 1 else 0
                top3_acc = results[2] if len(results) > 2 else 0

                report['models'][f'skin_{model_name}'] = {
                    'accuracy': float(accuracy),
                    'top3_accuracy': float(top3_acc),
                    'model_file': model_file,
                    'classes': len(class_names)
                }

                print(".4f")
                print(".4f")

            except Exception as e:
                print(f"   ❌ Error loading {model_name}: {e}")

    # 3. Analyze X-ray Models
    print("\n📊 Analyzing X-ray Models...")
    xray_models = {}
    for file in os.listdir('.'):
        if file.startswith(('efficientnet_xray_model_', 'mobilenet_xray_model_')) and file.endswith('.h5'):
            model_name = file.split('_')[0]
            xray_models[model_name] = file

    if xray_models:
        # Load test data
        test_datagen = ImageDataGenerator(rescale=1./255)
        test_generator = test_datagen.flow_from_directory(
            'data/datasets/chest_xray/test',
            target_size=(224, 224),
            batch_size=32,
            class_mode='binary',
            shuffle=False
        )

        for model_name, model_file in xray_models.items():
            print(f"   Analyzing {model_name}...")
            try:
                model = tf.keras.models.load_model(model_file)
                results = model.evaluate(test_generator, verbose=0)

                # Get predictions
                predictions = model.predict(test_generator, verbose=0)
                y_true = test_generator.classes
                y_pred = (predictions > 0.5).astype(int).flatten()

                # Calculate metrics
                accuracy = results[1] if len(results) > 1 else 0
                precision = results[2] if len(results) > 2 else 0
                recall = results[3] if len(results) > 3 else 0
                auc = results[4] if len(results) > 4 else 0

                report['models'][f'xray_{model_name}'] = {
                    'accuracy': float(accuracy),
                    'precision': float(precision),
                    'recall': float(recall),
                    'auc': float(auc),
                    'model_file': model_file
                }

                print(".4f")
                print(".4f")
                print(".4f")

            except Exception as e:
                print(f"   ❌ Error loading {model_name}: {e}")

    # Generate comprehensive report
    print("\n📋 Generating Comprehensive Report...")

    # Create summary table
    summary_data = []
    for model_type, results in report['models'].items():
        row = {'Model_Type': model_type}
        if 'accuracy' in results:
            row['Accuracy'] = ".4f"
        if 'precision' in results:
            row['Precision'] = ".4f"
        if 'recall' in results:
            row['Recall'] = ".4f"
        if 'auc' in results:
            row['AUC'] = ".4f"
        if 'top3_accuracy' in results:
            row['Top3_Accuracy'] = ".4f"
        if 'cv_mean' in results:
            row['CV_Accuracy'] = ".4f"
        summary_data.append(row)

    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        print("\n📊 Model Performance Summary:")
        print(summary_df.to_string(index=False))

        # Save to CSV
        summary_df.to_csv(f'model_performance_summary_{timestamp}.csv', index=False)

    # Save full report
    with open(f'comprehensive_model_report_{timestamp}.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)

    # Create visualizations
    create_performance_plots(report, timestamp)

    print("
✅ Analysis Complete!"    print(f"📁 Report saved as: comprehensive_model_report_{timestamp}.json")
    print(f"📊 Summary saved as: model_performance_summary_{timestamp}.csv")
    print(f"📈 Plots saved with timestamp: {timestamp}")

    return report

def create_performance_plots(report, timestamp):
    """Create performance comparison plots"""
    try:
        # Accuracy comparison
        accuracies = {}
        for model_type, results in report['models'].items():
            if 'accuracy' in results:
                accuracies[model_type] = results['accuracy']

        if accuracies:
            plt.figure(figsize=(12, 6))
            models = list(accuracies.keys())
            acc_values = list(accuracies.values())

            bars = plt.bar(models, acc_values, color=['skyblue', 'lightgreen', 'lightcoral', 'gold'])
            plt.title('Model Accuracy Comparison', fontsize=16)
            plt.ylabel('Accuracy', fontsize=12)
            plt.xlabel('Models', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3)

            # Add value labels on bars
            for bar, value in zip(bars, acc_values):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        ".3f", ha='center', va='bottom', fontsize=10)

            plt.tight_layout()
            plt.savefig(f'model_accuracy_comparison_{timestamp}.png', dpi=300, bbox_inches='tight')
            plt.show()

        # Medical metrics for X-ray models
        xray_metrics = {}
        for model_type, results in report['models'].items():
            if model_type.startswith('xray_'):
                xray_metrics[model_type] = {
                    'Precision': results.get('precision', 0),
                    'Recall': results.get('recall', 0),
                    'AUC': results.get('auc', 0)
                }

        if xray_metrics:
            fig, axes = plt.subplots(1, 3, figsize=(18, 6))
            metrics = ['Precision', 'Recall', 'AUC']
            models = list(xray_metrics.keys())

            for i, metric in enumerate(metrics):
                values = [xray_metrics[model][metric] for model in models]
                bars = axes[i].bar(models, values, color=['lightblue', 'lightgreen'])
                axes[i].set_title(f'{metric} Comparison', fontsize=14)
                axes[i].set_ylabel(metric, fontsize=12)
                axes[i].grid(True, alpha=0.3)

                for bar, value in zip(bars, values):
                    axes[i].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                               ".3f", ha='center', va='bottom', fontsize=10)

            plt.tight_layout()
            plt.savefig(f'xray_metrics_comparison_{timestamp}.png', dpi=300, bbox_inches='tight')
            plt.show()

    except Exception as e:
        print(f"⚠️ Error creating plots: {e}")

if __name__ == "__main__":
    analyze_all_models()