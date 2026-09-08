import pandas as pd
from sqlalchemy import create_engine

DB_URL = "postgresql://postgres:postgres@localhost:5432/gridsight"
engine = create_engine(DB_URL)

df = pd.read_csv("../data/cleaned_hourly.csv", index_col=0, parse_dates=True)
readings = df[["Global_active_power", "Global_reactive_power", "Voltage",
               "Global_intensity", "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]].copy()
readings.columns = ["global_active_power", "global_reactive_power", "voltage",
                     "global_intensity", "sub_metering_1", "sub_metering_2", "sub_metering_3"]
readings["timestamp"] = readings.index
readings["source"] = "uci"

readings.to_sql("readings", engine, if_exists="append", index=False)
print(f"Loaded {len(readings)} rows into the readings table")