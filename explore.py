import pandas as pd

df = pd.read_csv(
    "../data/household_power_consumption.txt",
    sep=";",
    na_values=["?"],
    low_memory=False
)

print(df.shape)
print(df.head())
print(df.dtypes)
print(df.isna().sum())


df["datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="%d/%m/%Y %H:%M:%S")

numeric_cols = ["Global_active_power", "Global_reactive_power", "Voltage",
                 "Global_intensity", "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print(df["datetime"].min(), "to", df["datetime"].max())
print(f"Missing rows: {df.isna().any(axis=1).sum()} ({df.isna().any(axis=1).mean()*100:.2f}%)")