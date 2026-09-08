CREATE TABLE readings (
    reading_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    global_active_power FLOAT,
    global_reactive_power FLOAT,
    voltage FLOAT,
    global_intensity FLOAT,
    sub_metering_1 FLOAT,
    sub_metering_2 FLOAT,
    sub_metering_3 FLOAT,
    source VARCHAR(20) DEFAULT 'uci'
);

CREATE TABLE daily_features (
    date DATE PRIMARY KEY,
    total_kwh FLOAT,
    peak_hour INT,
    peak_to_avg_ratio FLOAT,
    weekday_flag BOOLEAN,
    season INT,
    rolling_7d_avg FLOAT,
    cluster_label VARCHAR(30)
);

CREATE INDEX idx_readings_timestamp ON readings(timestamp);