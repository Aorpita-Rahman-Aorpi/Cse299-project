import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11

# Load data
df = pd.read_csv('diabetes.csv')

print("Creating visualizations...")

# GRAPH 1: Diabetes Distribution (Bar Chart)
plt.figure(figsize=(10, 6))
diabetes_counts = df['Outcome'].value_counts()
colors = ['#2ecc71', '#e74c3c']
bars = plt.bar(['No Diabetes', 'Has Diabetes'], diabetes_counts.values, color=colors, edgecolor='black', linewidth=2)
plt.title('Diabetes Distribution in Dataset', fontsize=16, fontweight='bold', pad=20)
plt.ylabel('Number of Patients', fontsize=12)
plt.xlabel('Diabetes Status', fontsize=12)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)} ({height/len(df)*100:.1f}%)',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('graph1_diabetes_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Graph 1 created: Diabetes Distribution")

# GRAPH 2: Age Distribution (Histogram)
plt.figure(figsize=(10, 6))
plt.hist(df['Age'], bins=30, color='#3498db', edgecolor='black', alpha=0.7)
plt.axvline(df['Age'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["Age"].mean():.1f} years')
plt.title('Age Distribution of Patients', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Age (years)', fontsize=12)
plt.ylabel('Number of Patients', fontsize=12)
plt.legend(fontsize=11)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('graph2_age_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Graph 2 created: Age Distribution")

# GRAPH 3: Glucose vs Age Scatter Plot
plt.figure(figsize=(12, 6))
diabetic = df[df['Outcome'] == 1]
non_diabetic = df[df['Outcome'] == 0]

plt.scatter(non_diabetic['Age'], non_diabetic['Glucose'], 
           c='#2ecc71', label='No Diabetes', alpha=0.6, s=50, edgecolor='black', linewidth=0.5)
plt.scatter(diabetic['Age'], diabetic['Glucose'], 
           c='#e74c3c', label='Has Diabetes', alpha=0.6, s=50, edgecolor='black', linewidth=0.5)

plt.title('Glucose Level vs Age (Colored by Diabetes Status)', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Age (years)', fontsize=12)
plt.ylabel('Glucose Level (mg/dL)', fontsize=12)
plt.legend(fontsize=11, loc='upper left')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('graph3_glucose_vs_age.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Graph 3 created: Glucose vs Age")

# GRAPH 4: BMI Comparison (Box Plot)
plt.figure(figsize=(10, 6))
data_to_plot = [non_diabetic['BMI'].dropna(), diabetic['BMI'].dropna()]
box = plt.boxplot(data_to_plot, labels=['No Diabetes', 'Has Diabetes'], 
                  patch_artist=True, notch=True, widths=0.6)

# Color the boxes
colors = ['#2ecc71', '#e74c3c']
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

plt.title('BMI Comparison: Diabetic vs Non-Diabetic', fontsize=16, fontweight='bold', pad=20)
plt.ylabel('BMI (Body Mass Index)', fontsize=12)
plt.xlabel('Diabetes Status', fontsize=12)
plt.grid(axis='y', alpha=0.3)

# Add mean values
means = [non_diabetic['BMI'].mean(), diabetic['BMI'].mean()]
plt.plot([1, 2], means, 'D-', color='black', linewidth=2, markersize=8, label='Mean BMI')
plt.legend(fontsize=10)

plt.tight_layout()
plt.savefig('graph4_bmi_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Graph 4 created: BMI Comparison")

# GRAPH 5: Correlation Heatmap
plt.figure(figsize=(12, 8))
correlation = df.corr()
sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', 
            center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Feature Correlation Heatmap', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('graph5_correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Graph 5 created: Correlation Heatmap")

# GRAPH 6: Feature Comparison (Multiple Features)
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
features = ['Glucose', 'BMI', 'Age', 'BloodPressure', 'Insulin', 'Pregnancies']

for idx, feature in enumerate(features):
    row = idx // 3
    col = idx % 3
    
    diabetic_data = df[df['Outcome'] == 1][feature].dropna()
    non_diabetic_data = df[df['Outcome'] == 0][feature].dropna()
    
    axes[row, col].hist([non_diabetic_data, diabetic_data], 
                        bins=20, label=['No Diabetes', 'Has Diabetes'],
                        color=['#2ecc71', '#e74c3c'], alpha=0.7, edgecolor='black')
    axes[row, col].set_title(f'{feature} Distribution', fontweight='bold')
    axes[row, col].set_xlabel(feature)
    axes[row, col].set_ylabel('Frequency')
    axes[row, col].legend()
    axes[row, col].grid(alpha=0.3)

plt.suptitle('Feature Distributions: Diabetic vs Non-Diabetic', 
             fontsize=18, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig('graph6_feature_distributions.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Graph 6 created: Feature Distributions")

print("\n" + "="*70)
print("ALL VISUALIZATIONS CREATED SUCCESSFULLY!")
print("="*70)
print("\nFiles created:")
print("  1. graph1_diabetes_distribution.png")
print("  2. graph2_age_distribution.png")
print("  3. graph3_glucose_vs_age.png")
print("  4. graph4_bmi_comparison.png")
print("  5. graph5_correlation_heatmap.png")
print("  6. graph6_feature_distributions.png")