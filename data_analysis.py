import pandas as pd
import numpy as np

print("="*70)
print("DIABETES DATASET ANALYSIS")
print("="*70)

# Load the dataset
df = pd.read_csv('diabetes.csv')

# Basic information
print(f"\n1. DATASET SIZE:")
print(f"   Total patients: {len(df)}")
print(f"   Total features: {len(df.columns) - 1}")
print(f"   Columns: {list(df.columns)}")

# First few rows
print(f"\n2. FIRST 5 PATIENTS:")
print(df.head())

# Basic statistics
print(f"\n3. STATISTICAL SUMMARY:")
print(df.describe())

# Diabetes distribution
print(f"\n4. DIABETES DISTRIBUTION:")
diabetes_counts = df['Outcome'].value_counts()
print(f"   No Diabetes (0): {diabetes_counts[0]} patients ({diabetes_counts[0]/len(df)*100:.1f}%)")
print(f"   Has Diabetes (1): {diabetes_counts[1]} patients ({diabetes_counts[1]/len(df)*100:.1f}%)")

# Key patterns
print(f"\n5. KEY PATTERNS DISCOVERED:")
diabetic = df[df['Outcome'] == 1]
non_diabetic = df[df['Outcome'] == 0]

print(f"\n   GLUCOSE LEVELS:")
print(f"   - Diabetic patients: {diabetic['Glucose'].mean():.1f} mg/dL")
print(f"   - Non-diabetic patients: {non_diabetic['Glucose'].mean():.1f} mg/dL")
print(f"   - Difference: {diabetic['Glucose'].mean() - non_diabetic['Glucose'].mean():.1f} mg/dL (SIGNIFICANT!)")

print(f"\n   BMI (Body Mass Index):")
print(f"   - Diabetic patients: {diabetic['BMI'].mean():.1f}")
print(f"   - Non-diabetic patients: {non_diabetic['BMI'].mean():.1f}")
print(f"   - Difference: {diabetic['BMI'].mean() - non_diabetic['BMI'].mean():.1f}")

print(f"\n   AGE:")
print(f"   - Diabetic patients: {diabetic['Age'].mean():.1f} years")
print(f"   - Non-diabetic patients: {non_diabetic['Age'].mean():.1f} years")
print(f"   - Difference: {diabetic['Age'].mean() - non_diabetic['Age'].mean():.1f} years")

# Correlation analysis
print(f"\n6. FEATURE CORRELATIONS WITH DIABETES:")
correlations = df.corr()['Outcome'].sort_values(ascending=False)
print(correlations)

print(f"\n7. MISSING VALUES CHECK:")
print(df.isnull().sum())

print("\n" + "="*70)
print("ANALYSIS COMPLETE!")
print("="*70)

# Save summary to text file
with open('analysis_summary.txt', 'w') as f:
    f.write("DIABETES DATASET ANALYSIS SUMMARY\n")
    f.write("="*70 + "\n\n")
    f.write(f"Total Patients: {len(df)}\n")
    f.write(f"Diabetic: {diabetes_counts[1]} ({diabetes_counts[1]/len(df)*100:.1f}%)\n")
    f.write(f"Non-diabetic: {diabetes_counts[0]} ({diabetes_counts[0]/len(df)*100:.1f}%)\n\n")
    f.write("KEY FINDINGS:\n")
    f.write(f"- Glucose: Diabetic {diabetic['Glucose'].mean():.1f} vs Non-diabetic {non_diabetic['Glucose'].mean():.1f}\n")
    f.write(f"- BMI: Diabetic {diabetic['BMI'].mean():.1f} vs Non-diabetic {non_diabetic['BMI'].mean():.1f}\n")
    f.write(f"- Age: Diabetic {diabetic['Age'].mean():.1f} vs Non-diabetic {non_diabetic['Age'].mean():.1f}\n")

print("\n✅ Summary saved to 'analysis_summary.txt'")