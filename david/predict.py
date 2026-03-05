import requests
import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBRegressor

# ---------------------------------------
# 1. Fetch Kenya data from API
# ---------------------------------------

API_URL = "http://127.0.0.1:5000/api/mongo/range/Kenya?start=2018-01-01&end=2025-05-31"

response = requests.get(API_URL)
data = response.json()

df = pd.DataFrame(data)

# Convert date
df['date'] = pd.to_datetime(df['date'])

# Sort by date
df = df.sort_values("date")

print("Data retrieved from API")
print(df.head())


# ---------------------------------------
# 2. Create time-series lag features
# ---------------------------------------

df['pm25_lag1'] = df['pm25_ugm3'].shift(1)
df['pm25_lag2'] = df['pm25_ugm3'].shift(2)
df['pm25_lag3'] = df['pm25_ugm3'].shift(3)

df['temp_lag1'] = df['temperature_celsius'].shift(1)

df = df.dropna()


# ---------------------------------------
# 3. Define features and target
# ---------------------------------------

features = [
    "temperature_celsius",
    "pm25_ugm3",
    "pm25_lag1",
    "pm25_lag2",
    "pm25_lag3",
    "temp_lag1"
]

target = "respiratory_disease_rate"

X = df[features]
y = df[target]


# ---------------------------------------
# 4. Train XGBoost model
# ---------------------------------------

model = XGBRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=5,
    random_state=42
)

model.fit(X, y)

print("Model training completed")


# ---------------------------------------
# 5. Predict next respiratory disease rate
# ---------------------------------------

latest_data = X.iloc[-1:].copy()

prediction = model.predict(latest_data)

print("\nPredicted Respiratory Disease Rate (Next Period):")
print(round(prediction[0], 3))


# ---------------------------------------
# 6. Predict several future steps
# ---------------------------------------

future_predictions = []

current = latest_data.copy()

for i in range(6):  # predict next 6 weeks/months depending on dataset
    pred = model.predict(current)[0]
    future_predictions.append(pred)

print("\nFuture Respiratory Disease Predictions:")
print(future_predictions)


# ---------------------------------------
# 7. Visualization
# ---------------------------------------

plt.figure()

plt.plot(df["date"], df[target], label="Historical Respiratory Rate")

future_dates = pd.date_range(
    start=df["date"].iloc[-1],
    periods=6,
    freq="M"
)

plt.plot(future_dates, future_predictions, label="Forecast")

plt.xlabel("Date")
plt.ylabel("Respiratory Disease Rate")
plt.title("Respiratory Disease Forecast for Kenya")

plt.legend()

plt.show()