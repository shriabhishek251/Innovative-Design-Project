import pandas as pd
import numpy as np

def load_and_clean(path="../data/household_power_consumption.txt"):
    df = pd.read_csv(path, sep=";", na_values=["?"], low_memory=False)
    df["datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="%d/%m/%Y %H:%M:%S")
    df = df.drop(columns=["Date", "Time"]).set_index("datetime")

    numeric_cols = ["Global_active_power", "Global_reactive_power", "Voltage",
                     "Global_intensity", "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df[numeric_cols] = df[numeric_cols].ffill(limit=5)

    df["minute_of_day"] = df.index.hour * 60 + df.index.minute
    for col in numeric_cols:
        slot_means = df.groupby("minute_of_day")[col].transform("mean")
        df[col] = df[col].fillna(slot_means)
    df = df.drop(columns=["minute_of_day"])

    return df

def resample_hourly(df):
    hourly = df.resample("h").agg({
        "Global_active_power": "mean",
        "Global_reactive_power": "mean",
        "Voltage": "mean",
        "Global_intensity": "mean",
        "Sub_metering_1": "sum",
        "Sub_metering_2": "sum",
        "Sub_metering_3": "sum",
    })
    return hourly

def add_time_features(df):
    df = df.copy()
    df["hour"] = df.index.hour
    df["day_of_week"] = df.index.dayofweek
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
    df["month"] = df.index.month
    df["season"] = df["month"] % 12 // 3

    df["rolling_mean_24h"] = df["Global_active_power"].rolling(24, min_periods=1).mean()
    df["rolling_mean_7d"] = df["Global_active_power"].rolling(24*7, min_periods=1).mean()
    df["lag_1h"] = df["Global_active_power"].shift(1)
    df["lag_24h"] = df["Global_active_power"].shift(24)
    df["lag_168h"] = df["Global_active_power"].shift(168)

    return df

if __name__ == "__main__":
    raw = load_and_clean()
    hourly = resample_hourly(raw)
    featured = add_time_features(hourly)
    featured.to_csv("../data/cleaned_hourly.csv")
    print(f"Saved {len(featured)} rows to data/cleaned_hourly.csv")