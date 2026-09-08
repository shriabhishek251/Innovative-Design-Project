import os
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "..", "data", "cleaned_hourly.csv")

df = pd.read_csv(data_path, index_col=0, parse_dates=True)

# shift(1) FIRST, then roll — so the window only ever sees the past, never the current row
df["lag_2h"] = df["Global_active_power"].shift(2)
df["lag_3h"] = df["Global_active_power"].shift(3)
df["rolling_min_24h"] = df["Global_active_power"].shift(1).rolling(24, min_periods=1).min()
df["rolling_max_24h"] = df["Global_active_power"].shift(1).rolling(24, min_periods=1).max()
df["rolling_mean_3h"] = df["Global_active_power"].shift(1).rolling(3, min_periods=1).mean()

df = df.dropna(subset=["lag_1h", "lag_2h", "lag_3h", "lag_24h", "lag_168h"])

feature_cols = ["hour", "day_of_week", "is_weekend", "month",
                 "rolling_mean_24h", "rolling_mean_7d", "rolling_mean_3h",
                 "rolling_min_24h", "rolling_max_24h",
                 "lag_1h", "lag_2h", "lag_3h", "lag_24h", "lag_168h"]
X = df[feature_cols]
y = df["Global_active_power"]

cutoff = df.index.max() - pd.Timedelta(weeks=5)
X_train, X_test = X[df.index <= cutoff], X[df.index > cutoff]
y_train, y_test = y[df.index <= cutoff], y[df.index > cutoff]

model = xgb.XGBRegressor(n_estimators=300, max_depth=6, learning_rate=0.05, random_state=42)
persistence_mape = mean_absolute_percentage_error(y_test, X_test["lag_1h"]) * 100
print(f"Persistence baseline MAPE: {persistence_mape:.2f}%")
model.fit(X_train, y_train)

preds = model.predict(X_test)
mape = mean_absolute_percentage_error(y_test, preds) * 100
rmse = np.sqrt(mean_squared_error(y_test, preds))
mae = np.mean(np.abs(y_test - preds))
print(f"MAPE: {mape:.2f}%   RMSE: {rmse:.3f}   MAE: {mae:.3f} kW")

low_mask = y_test < y_test.median()
mape_low = mean_absolute_percentage_error(y_test[low_mask], preds[low_mask]) * 100
mape_high = mean_absolute_percentage_error(y_test[~low_mask], preds[~low_mask]) * 100
print(f"MAPE on below-median actual usage: {mape_low:.2f}%")
print(f"MAPE on above-median actual usage: {mape_high:.2f}%")

import joblib
model_path = os.path.join(script_dir, "..", "models", "forecasting_model.pkl")
features_path = os.path.join(script_dir, "..", "models", "forecasting_features.pkl")
joblib.dump(model, model_path)
joblib.dump(feature_cols, features_path)
print(f"Saved model to {model_path}")