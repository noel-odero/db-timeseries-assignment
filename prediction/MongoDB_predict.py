import requests
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("\n" + "="*70)
print("MONGODB PREDICTION SCRIPT - Using XGBoost Model")
print("="*70)

# ---------------------------------------
# 1. Fetch latest data (with fallback to CSV)
# ---------------------------------------
print("\nSTEP 1: Fetching latest data...")

API_URL = "http://127.0.0.1:5000/api/mongo/latest/Kenya"

try:
    response = requests.get(API_URL, timeout=5)
    if response.status_code == 200:
        record = response.json()
        print(f"   Successfully fetched data from MongoDB API")
    else:
        raise Exception("API returned error")
except Exception as e:
    print(f"   MongoDB API unavailable, using CSV data...")
    # Fallback: Read from CSV
    df = pd.read_csv('../data.csv')
    df['date'] = pd.to_datetime(df['date'])
    kenya_data = df[df['country_name'] == 'Kenya'].sort_values('date', ascending=False).iloc[0]
    record = {
        'date': kenya_data['date'].strftime('%Y-%m-%d'),
        'temperature_celsius': kenya_data['temperature_celsius'],
        'temp_anomaly_celsius': kenya_data.get('temp_anomaly_celsius', 0),
        'precipitation_mm': kenya_data.get('precipitation_mm', 0),
        'pm25_ugm3': kenya_data['pm25_ugm3'],
        'air_quality_index': kenya_data.get('air_quality_index', 0),
        'heat_wave_days': kenya_data.get('heat_wave_days', 0),
        'heat_related_admissions': kenya_data.get('heat_related_admissions', 0),
        'waterborne_disease_incidents': kenya_data.get('waterborne_disease_incidents', 0),
        'respiratory_disease_rate': kenya_data['respiratory_disease_rate'],
        'healthcare_access_index': kenya_data.get('healthcare_access_index', 65.0),
        'gdp_per_capita_usd': kenya_data.get('gdp_per_capita_usd', 2000)
    }
    print(f"   Loaded data from CSV")

print(f"   Date: {record['date']}")
print(f"   Temperature: {record['temperature_celsius']}°C")
print(f"   PM2.5: {record['pm25_ugm3']}")

# ---------------------------------------
# 2. Load trained XGBoost model
# ---------------------------------------
print("\nSTEP 2: Loading trained XGBoost model...")

model_path = '../models/xgboost_tuned.pkl'
model = joblib.load(model_path)
print(f"   Model loaded from {model_path}")

# ---------------------------------------
# 3. Preprocess data (matching Task 1C)
# ---------------------------------------
print("\nSTEP 3: Preprocessing data...")

date_obj = datetime.strptime(record['date'][:10], '%Y-%m-%d')

features = {}
features['temperature_celsius'] = float(record['temperature_celsius'])
features['temp_anomaly_celsius'] = float(record.get('temp_anomaly_celsius', 0))
features['precipitation_mm'] = float(record.get('precipitation_mm', 0))
features['pm25_ugm3'] = float(record['pm25_ugm3'])
features['air_quality_index'] = float(record.get('air_quality_index', 0))
features['heat_wave_days'] = float(record.get('heat_wave_days', 0))
features['heat_related_admissions'] = float(record.get('heat_related_admissions', 0))
features['waterborne_disease_incidents'] = float(record.get('waterborne_disease_incidents', 0))
features['healthcare_access_index'] = float(record.get('healthcare_access_index', 65.0))
features['gdp_per_capita_usd'] = float(record.get('gdp_per_capita_usd', 2000))
features['income_encoded'] = 1  # Kenya = Lower middle income
features['country_encoded'] = 10  # Kenya encoding

# Seasonal features
features['month_sin'] = np.sin(2 * np.pi * date_obj.month / 12)
features['month_cos'] = np.cos(2 * np.pi * date_obj.month / 12)
features['week_sin'] = np.sin(2 * np.pi * date_obj.isocalendar()[1] / 52)
features['week_cos'] = np.cos(2 * np.pi * date_obj.isocalendar()[1] / 52)

# Lag features (approximated)
features['pm25_lag1'] = features['pm25_ugm3'] * 0.95
features['pm25_lag2'] = features['pm25_ugm3'] * 0.92
features['pm25_lag4'] = features['pm25_ugm3'] * 0.88
features['pm25_lag8'] = features['pm25_ugm3'] * 0.85
features['pm25_lag12'] = features['pm25_ugm3'] * 0.82
features['pm25_lag26'] = features['pm25_ugm3'] * 0.78
features['temp_lag1'] = features['temperature_celsius'] * 0.97
features['temp_lag4'] = features['temperature_celsius'] * 0.94
features['temp_lag8'] = features['temperature_celsius'] * 0.90

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

# Interactions
features['temp_x_pm25'] = features['temperature_celsius'] * features['pm25_ugm3']
features['pm25_x_precip'] = features['pm25_ugm3'] * features['precipitation_mm']

# ---------------------------------------
# 4. Create feature vector
# ---------------------------------------
print("\nSTEP 4: Creating feature vector...")

feature_cols = [
    'temperature_celsius', 'temp_anomaly_celsius', 'precipitation_mm',
    'pm25_ugm3', 'air_quality_index', 'heat_wave_days',
    'heat_related_admissions', 'waterborne_disease_incidents',
    'healthcare_access_index', 'gdp_per_capita_usd',
    'income_encoded', 'country_encoded',
    'month_sin', 'month_cos', 'week_sin', 'week_cos',
    'pm25_lag1', 'pm25_lag2', 'pm25_lag4', 'pm25_lag8', 'pm25_lag12', 'pm25_lag26',
    'temp_lag1', 'temp_lag4', 'temp_lag8',
    'resp_lag1', 'resp_lag2', 'resp_lag4', 'resp_lag8',
    'pm25_ma4', 'pm25_ma8', 'temp_ma4', 'temp_ma8', 'temp_ma12', 'resp_ma4',
    'temp_x_pm25', 'pm25_x_precip'
]

X_pred = np.array([[features[col] for col in feature_cols]])
print(f"   Feature vector created with {len(feature_cols)} features")

# ---------------------------------------
# 5. Make prediction
# ---------------------------------------
print("\nSTEP 5: Making prediction...")

prediction = model.predict(X_pred)[0]

print("\n" + "="*70)
print("PREDICTION RESULT")
print("="*70)
print(f"Country: Kenya")
print(f"Date: {record['date']}")
print(f"Temperature: {features['temperature_celsius']:.2f}°C")
print(f"PM2.5: {features['pm25_ugm3']:.2f}")
print(f"Current Respiratory Rate: {current_resp:.2f}")
print("-" * 70)
print(f"   Predicted Respiratory Disease Rate: {prediction:.2f} per 100,000")
print("="*70)

# Save result
result_text = f"""
{'='*70}
MONGODB PREDICTION RESULT - XGBoost Model
{'='*70}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

INPUT DATA:
  Country: Kenya
  Date: {record['date']}
  Temperature: {features['temperature_celsius']:.2f}°C
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

with open('prediction_result.txt', 'w') as f:
    f.write(result_text)

print("\n   Result saved to 'prediction_result.txt'")
print("\n   PREDICTION COMPLETE!")