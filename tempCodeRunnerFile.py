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