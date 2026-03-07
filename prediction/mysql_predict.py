# ============================================
# mysql_predict.py - Task 4 Prediction Script
# best model file name: xgboost_tuned.pkl
# ============================================

import requests
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

print("\n" + "="*70)
print("TASK 4: PREDICTION SCRIPT (Using XGBoost model from Task 1C)")
print("="*70)

# ============================================
# STEP 1: Fetch data from your MySQL API
# ============================================
print("\nSTEP 1: Fetching latest data from MySQL API...")

API_URL = "http://127.0.0.1:5000/api/mysql/latest/USA"

try:
    response = requests.get(API_URL)
    data = response.json()
    
    if data.get('success'):
        record = data['data']
        print(f"   Successfully fetched data for {record['country_name']}")
        print(f"   Date: {record['date']}")
        print(f"   Temperature: {record['temperature_celsius']}°C")
        print(f"   Precipitation: {record.get('precipitation_mm', 0)}mm")
        print(f"   PM2.5: {record.get('pm25_ugm3', 0)}")
        print(f"   Respiratory Rate: {record['respiratory_disease_rate']}")
    else:
        print(f" API error: {data.get('error', 'Unknown error')}")
        exit()
        
except requests.exceptions.ConnectionError:
    print(" Cannot connect to API. Make sure your API is running!")
    print("   Run: python mysql_api/app.py")
    exit()
except Exception as e:
    print(f" Error: {e}")
    exit()

# ============================================
# STEP 2: Load YOUR trained XGBoost model
# ============================================
print("\n STEP 2: Loading your trained XGBoost model...")

# Your model filename
MODEL_FILENAME = "xgboost_tuned.pkl"
model_path = f'../models/{MODEL_FILENAME}'

if os.path.exists(model_path):
    model = joblib.load(model_path)
    print(f"Model loaded from {model_path}")
else:
    print(f"Model not found at {model_path}")
    print("\n   Please make sure your model is in the 'models' folder")
    exit()

# ============================================
# STEP 3: Preprocess data (EXACTLY like Task 1C)
# ============================================
print("\nSTEP 3: Preprocessing data (matching Task 1C features)...")

# Parse date
date_obj = datetime.strptime(record['date'], '%Y-%m-%d')

# Create feature dictionary matching your Task 1C feature_cols
features = {}

# Raw climate (from API response)
features['temperature_celsius'] = float(record['temperature_celsius'])
features['temp_anomaly_celsius'] = float(record.get('temp_anomaly_celsius', 0))
features['precipitation_mm'] = float(record.get('precipitation_mm', 0))
features['pm25_ugm3'] = float(record.get('pm25_ugm3', 0))
features['air_quality_index'] = float(record.get('air_quality_index', 0))
features['heat_wave_days'] = float(record.get('heat_wave_days', 0))
features['heat_related_admissions'] = float(record.get('heat_related_admissions', 0))
features['waterborne_disease_incidents'] = float(record.get('waterborne_disease_incidents', 0))

# Socioeconomic (from API)
features['healthcare_access_index'] = float(record.get('healthcare_access_index', 77.3))
features['gdp_per_capita_usd'] = float(record.get('gdp_per_capita_usd', 63627))

# Encoded categoricals (based on your training data)
# USA = High income, country_code 'USA'
features['income_encoded'] = 2  # High income typically encoded as 2
features['country_encoded'] = 23  # USA's encoding (based on alphabetical order)

# Seasonal features (calculated from date)
features['month_sin'] = np.sin(2 * np.pi * date_obj.month / 12)
features['month_cos'] = np.cos(2 * np.pi * date_obj.month / 12)
features['week_sin'] = np.sin(2 * np.pi * date_obj.isocalendar()[1] / 52)
features['week_cos'] = np.cos(2 * np.pi * date_obj.isocalendar()[1] / 52)

# PM2.5 lags (approximated from current value)
features['pm25_lag1'] = features['pm25_ugm3'] * 0.95
features['pm25_lag2'] = features['pm25_ugm3'] * 0.92
features['pm25_lag4'] = features['pm25_ugm3'] * 0.88
features['pm25_lag8'] = features['pm25_ugm3'] * 0.85
features['pm25_lag12'] = features['pm25_ugm3'] * 0.82
features['pm25_lag26'] = features['pm25_ugm3'] * 0.78

# Temperature lags
features['temp_lag1'] = features['temperature_celsius'] * 0.97
features['temp_lag4'] = features['temperature_celsius'] * 0.94
features['temp_lag8'] = features['temperature_celsius'] * 0.90

# Autoregressive lags (respiratory rate lags)
current_resp = float(record['respiratory_disease_rate'])
features['resp_lag1'] = current_resp * 0.98
features['resp_lag2'] = current_resp * 0.96
features['resp_lag4'] = current_resp * 0.94
features['resp_lag8'] = current_resp * 0.92

# Moving averages
features['pm25_ma4'] = features['pm25_ugm3'] * 0.96
features['pm25_ma8'] = features['pm25_ugm3'] * 0.94
features['temp_ma4'] = features['temperature_celsius'] * 0.98
features['temp_ma8'] = features['temperature_celsius'] * 0.96
features['temp_ma12'] = features['temperature_celsius'] * 0.95
features['resp_ma4'] = current_resp * 0.97

# Interaction features
features['temp_x_pm25'] = features['temperature_celsius'] * features['pm25_ugm3']
features['pm25_x_precip'] = features['pm25_ugm3'] * features['precipitation_mm']

# ============================================
# STEP 4: Create feature vector in correct order
# ============================================
print("\nSTEP 4: Creating feature vector...")

# EXACT feature order from your Task 1C
feature_cols = [
    # Raw climate
    'temperature_celsius', 'temp_anomaly_celsius', 'precipitation_mm',
    'pm25_ugm3', 'air_quality_index', 'heat_wave_days',
    'heat_related_admissions', 'waterborne_disease_incidents',
    # Socioeconomic
    'healthcare_access_index', 'gdp_per_capita_usd',
    # Encoded categoricals
    'income_encoded', 'country_encoded',
    # Seasonal
    'month_sin', 'month_cos', 'week_sin', 'week_cos',
    # PM2.5 lags
    'pm25_lag1', 'pm25_lag2', 'pm25_lag4', 'pm25_lag8', 'pm25_lag12', 'pm25_lag26',
    # Temperature lags
    'temp_lag1', 'temp_lag4', 'temp_lag8',
    # Autoregressive lags
    'resp_lag1', 'resp_lag2', 'resp_lag4', 'resp_lag8',
    # Moving averages
    'pm25_ma4', 'pm25_ma8', 'temp_ma4', 'temp_ma8', 'temp_ma12', 'resp_ma4',
    # Interactions
    'temp_x_pm25', 'pm25_x_precip'
]

# Create feature array
feature_vector = []
missing_features = []
for col in feature_cols:
    if col in features:
        feature_vector.append(features[col])
    else:
        print(f"Warning: {col} not found, using 0")
        feature_vector.append(0.0)
        missing_features.append(col)

X_pred = np.array([feature_vector])
print(f"Feature vector created with {len(feature_cols)} features")
if missing_features:
    print(f"   Note: {len(missing_features)} features used defaults")

# ============================================
# STEP 5: Make prediction
# ============================================
print("\nSTEP 5: Making prediction...")

prediction = model.predict(X_pred)[0]
print(f"Prediction complete!")

# ============================================
# STEP 6: Display and save results
# ============================================
print("\n" + "="*70)
print("PREDICTION RESULT")
print("="*70)
print(f"Country: {record['country_name']}")
print(f"Date: {record['date']}")
print(f"Temperature: {features['temperature_celsius']:.2f}°C")
print(f"Precipitation: {features['precipitation_mm']:.2f}mm")
print(f"PM2.5: {features['pm25_ugm3']:.2f}")
print(f"Current Respiratory Rate: {current_resp:.2f}")
print("-" * 70)
print(f" Predicted Respiratory Disease Rate: {prediction:.2f} per 100,000")
print("="*70)

# Create result text
result_text = f"""
{'='*70}
TASK 4 PREDICTION RESULT - XGBoost Model (xgboost_tuned.pkl)
{'='*70}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

INPUT DATA:
  Country: {record['country_name']}
  Date: {record['date']}
  Temperature: {features['temperature_celsius']:.2f}°C
  Precipitation: {features['precipitation_mm']:.2f}mm
  PM2.5: {features['pm25_ugm3']:.2f}
  Current Respiratory Rate: {current_resp:.2f}

PREDICTION:
  Respiratory Disease Rate: {prediction:.2f} per 100,000

MODEL INFO:
  Model: XGBoost Regressor (tuned)
  Model File: xgboost_tuned.pkl
  Features Used: {len(feature_cols)}
{'='*70}
"""

# Save to file
output_path = 'prediction_result.txt'
with open(output_path, 'w') as f:
    f.write(result_text)

print(f"\n Result saved to '{output_path}'")
print("\n TASK 4 COMPLETE!")