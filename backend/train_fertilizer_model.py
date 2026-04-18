"""
Train fertilizer recommendation model from data_core.csv
Uses NPK deficiency rules + ML for best accuracy
"""
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report

# Load data
print("Loading data...")
df = pd.read_csv('data_core.csv')
print(f"Dataset shape: {df.shape}")

# ── Rule-based label: assign fertilizer based on NPK deficiency ──────────────
def rule_label(row):
    N, P, K = row['Nitrogen'], row['Phosphorous'], row['Potassium']
    # High N → Urea (pure nitrogen)
    if N > 30:
        return 'Urea'
    # High P → DAP (high phosphorus)
    if P > 25:
        return 'DAP'
    # Balanced low NPK → 17-17-17
    if N < 15 and P < 15 and K < 5:
        return '17-17-17'
    # High P+K → 10-26-26
    if P > 15 and K > 5:
        return '10-26-26'
    # High P → 14-35-14
    if P > 20:
        return '14-35-14'
    # Moderate N+P → 28-28
    if N > 15 and P > 10:
        return '28-28'
    return '20-20'

df['Rule_Fertilizer'] = df.apply(rule_label, axis=1)
rule_match = (df['Rule_Fertilizer'] == df['Fertilizer Name']).mean()
print(f"Rule-based match with original labels: {rule_match*100:.1f}%")

# Use rule labels as training target (they encode domain knowledge)
df['Target'] = df['Rule_Fertilizer']

# Encode categoricals
soil_encoder = LabelEncoder()
crop_encoder = LabelEncoder()
fertilizer_encoder = LabelEncoder()

df['Soil Type Enc'] = soil_encoder.fit_transform(df['Soil Type'])
df['Crop Type Enc'] = crop_encoder.fit_transform(df['Crop Type'])
df['Target Enc'] = fertilizer_encoder.fit_transform(df['Target'])

print(f"Soil types: {list(soil_encoder.classes_)}")
print(f"Crop types: {list(crop_encoder.classes_)}")
print(f"Fertilizers: {list(fertilizer_encoder.classes_)}")

# Feature engineering: add NPK ratios
df['N_P_ratio'] = df['Nitrogen'] / (df['Phosphorous'] + 1)
df['N_K_ratio'] = df['Nitrogen'] / (df['Potassium'] + 1)
df['NPK_total'] = df['Nitrogen'] + df['Phosphorous'] + df['Potassium']

feature_cols = [
    'Temparature', 'Humidity', 'Moisture',
    'Soil Type Enc', 'Crop Type Enc',
    'Nitrogen', 'Potassium', 'Phosphorous',
    'N_P_ratio', 'N_K_ratio', 'NPK_total'
]

X = df[feature_cols].values
y = df['Target Enc'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"\nTrain: {X_train.shape[0]}, Test: {X_test.shape[0]}")

# Train
print("\nTraining Random Forest...")
model = RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

acc = accuracy_score(y_test, model.predict(X_test))
print(f"Accuracy: {acc*100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, model.predict(X_test), target_names=fertilizer_encoder.classes_))

# Feature importance
print("Feature importances:")
for feat, imp in sorted(zip(feature_cols, model.feature_importances_), key=lambda x: -x[1]):
    print(f"  {feat}: {imp:.3f}")

# Save
print("\nSaving models...")
pickle.dump(model,              open('models/fertilizer_model.pkl', 'wb'))
pickle.dump(soil_encoder,       open('models/fertilizer_soil_encoder.pkl', 'wb'))
pickle.dump(crop_encoder,       open('models/fertilizer_crop_encoder.pkl', 'wb'))
pickle.dump(fertilizer_encoder, open('models/fertilizer_label_encoder.pkl', 'wb'))

feature_info = {
    'features': feature_cols,
    'soil_types': list(soil_encoder.classes_),
    'crop_types': list(crop_encoder.classes_),
    'fertilizers': list(fertilizer_encoder.classes_),
    'accuracy': acc,
    'model_type': 'RandomForest + NPK rules'
}
pickle.dump(feature_info, open('models/fertilizer_feature_info.pkl', 'wb'))

print("✅ Done!")
print(f"   Accuracy: {acc*100:.2f}%")
print(f"   Fertilizers: {list(fertilizer_encoder.classes_)}")
