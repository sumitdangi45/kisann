import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
print("Loading data...")
df = pd.read_csv('Data/Data-processed/crop_recommendation.csv')

print("\n=== DATA OVERVIEW ===")
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nMissing values:\n{df.isnull().sum()}")

print("\n=== CROP DISTRIBUTION ===")
print(df['label'].value_counts())
print(f"Total unique crops: {df['label'].nunique()}")

print("\n=== STATISTICAL SUMMARY ===")
print(df.describe())

# Prepare data
print("\n=== PREPARING DATA ===")
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']

print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"\nTraining set size: {len(X_train)}")
print(f"Testing set size: {len(X_test)}")

# Train model
print("\n=== TRAINING MODEL ===")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)
print("Model training completed!")

# Evaluate model
print("\n=== MODEL EVALUATION ===")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")

# Feature importance
print("\n=== FEATURE IMPORTANCE ===")
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(feature_importance)

# Save model
print("\n=== SAVING MODEL ===")
model_path = 'models/crop_model_trained.pkl'
pickle.dump(model, open(model_path, 'wb'))
print(f"Model saved to: {model_path}")

# Save feature names
feature_names_path = 'models/crop_features.pkl'
pickle.dump(X.columns.tolist(), open(feature_names_path, 'wb'))
print(f"Feature names saved to: {feature_names_path}")

# Save label encoder
label_encoder = LabelEncoder()
label_encoder.fit(y)
encoder_path = 'models/crop_encoder.pkl'
pickle.dump(label_encoder, open(encoder_path, 'wb'))
print(f"Label encoder saved to: {encoder_path}")

print("\n=== TRAINING COMPLETE ===")
print(f"Model Accuracy: {accuracy*100:.2f}%")
print(f"Total crops: {len(label_encoder.classes_)}")
print(f"Crops: {', '.join(label_encoder.classes_)}")
