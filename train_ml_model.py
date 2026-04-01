import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

print("="*70)
print("MACHINE LEARNING MODEL TRAINING")
print("="*70)

# Load data
df = pd.read_csv('diabetes.csv')

# Prepare data
X = df.drop('Outcome', axis=1)  # Features
y = df['Outcome']  # Target

print(f"\n1. DATA PREPARATION:")
print(f"   Features shape: {X.shape}")
print(f"   Target shape: {y.shape}")
print(f"   Features: {list(X.columns)}")

# Split data (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n2. TRAIN-TEST SPLIT:")
print(f"   Training samples: {len(X_train)} ({len(X_train)/len(df)*100:.1f}%)")
print(f"   Testing samples: {len(X_test)} ({len(X_test)/len(df)*100:.1f}%)")
print(f"   Training diabetes cases: {y_train.sum()} ({y_train.mean()*100:.1f}%)")
print(f"   Testing diabetes cases: {y_test.sum()} ({y_test.mean()*100:.1f}%)")

# MODEL 1: LOGISTIC REGRESSION 
print(f"\n3. TRAINING MODEL 1: LOGISTIC REGRESSION")
print("   Training in progress...")

lr_model = LogisticRegression(random_state=42, max_iter=1000)
lr_model.fit(X_train, y_train)

lr_pred = lr_model.predict(X_test)
lr_accuracy = accuracy_score(y_test, lr_pred)

print(f"   ✓ Training complete!")
print(f"   Accuracy: {lr_accuracy*100:.2f}%")

#  MODEL 2: RANDOM FOREST 
print(f"\n4. TRAINING MODEL 2: RANDOM FOREST")
print("   Training in progress...")

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_pred)

print(f"   ✓ Training complete!")
print(f"   Accuracy: {rf_accuracy*100:.2f}%")

# MODEL COMPARISON 
print(f"\n5. MODEL COMPARISON:")
print(f"   Logistic Regression: {lr_accuracy*100:.2f}%")
print(f"   Random Forest:       {rf_accuracy*100:.2f}%")
print(f"   Winner: {'Random Forest' if rf_accuracy > lr_accuracy else 'Logistic Regression'} ")

#  DETAILED EVALUATION 
print(f"\n6. RANDOM FOREST DETAILED RESULTS:")
print("\n   Classification Report:")
print(classification_report(y_test, rf_pred, target_names=['No Diabetes', 'Has Diabetes']))

# Confusion Matrix
cm = confusion_matrix(y_test, rf_pred)
print(f"\n   Confusion Matrix:")
print(f"   {cm}")
print(f"\n   Interpretation:")
print(f"   - True Negatives (Correct 'No Diabetes'):  {cm[0,0]}")
print(f"   - False Positives (Wrong 'Has Diabetes'):  {cm[0,1]}")
print(f"   - False Negatives (Wrong 'No Diabetes'):   {cm[1,0]}")
print(f"   - True Positives (Correct 'Has Diabetes'): {cm[1,1]}")

# Feature Importance
print(f"\n7. FEATURE IMPORTANCE (Random Forest):")
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

print(feature_importance.to_string(index=False))

# VISUALIZATIONS

# Confusion Matrix Visualization
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True,
            xticklabels=['No Diabetes', 'Has Diabetes'],
            yticklabels=['No Diabetes', 'Has Diabetes'])
plt.title('Random Forest - Confusion Matrix', fontsize=16, fontweight='bold', pad=20)
plt.ylabel('True Label', fontsize=12)
plt.xlabel('Predicted Label', fontsize=12)
plt.tight_layout()
plt.savefig('ml_confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.close()
print("\n✓ Confusion matrix saved to 'ml_confusion_matrix.png'")

# Feature Importance Visualization
plt.figure(figsize=(10, 6))
plt.barh(feature_importance['Feature'], feature_importance['Importance'], color='#3498db', edgecolor='black')
plt.xlabel('Importance Score', fontsize=12)
plt.title('Feature Importance (Random Forest)', fontsize=16, fontweight='bold', pad=20)
plt.gca().invert_yaxis()
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('ml_feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Feature importance saved to 'ml_feature_importance.png'")

# Model Comparison Visualization
plt.figure(figsize=(10, 6))
models = ['Logistic\nRegression', 'Random\nForest']
accuracies = [lr_accuracy*100, rf_accuracy*100]
colors = ['#e74c3c', '#2ecc71']

bars = plt.bar(models, accuracies, color=colors, edgecolor='black', linewidth=2, width=0.6)
plt.title('Model Accuracy Comparison', fontsize=16, fontweight='bold', pad=20)
plt.ylabel('Accuracy (%)', fontsize=12)
plt.ylim(0, 100)
plt.grid(axis='y', alpha=0.3)

# Add value labels
for bar, acc in zip(bars, accuracies):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{acc:.2f}%',
             ha='center', va='bottom', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('ml_model_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Model comparison saved to 'ml_model_comparison.png'")

# Save model results to text file
with open('ml_results.txt', 'w') as f:
    f.write("MACHINE LEARNING RESULTS\n")
    f.write("="*70 + "\n\n")
    f.write(f"Dataset: {len(df)} patients\n")
    f.write(f"Training: {len(X_train)} samples\n")
    f.write(f"Testing: {len(X_test)} samples\n\n")
    f.write("MODEL PERFORMANCE:\n")
    f.write(f"1. Logistic Regression: {lr_accuracy*100:.2f}%\n")
    f.write(f"2. Random Forest:       {rf_accuracy*100:.2f}%\n\n")
    f.write("CONFUSION MATRIX (Random Forest):\n")
    f.write(f"True Negatives:  {cm[0,0]}\n")
    f.write(f"False Positives: {cm[0,1]}\n")
    f.write(f"False Negatives: {cm[1,0]}\n")
    f.write(f"True Positives:  {cm[1,1]}\n\n")
    f.write("TOP 3 IMPORTANT FEATURES:\n")
    for idx, row in feature_importance.head(3).iterrows():
        f.write(f"{idx+1}. {row['Feature']}: {row['Importance']:.4f}\n")

print("✓ Results saved to 'ml_results.txt'")

print("\n" + "="*70)
print("MACHINE LEARNING TRAINING COMPLETE!")
print("="*70)
print(f"\nBest Model: Random Forest with {rf_accuracy*100:.2f}% accuracy")
print("Ready to show Sir! 🎉")