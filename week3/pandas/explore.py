from pathlib import Path
import pandas as pd

path = Path(__file__).parent.parent / "sql-practice" / "data" / "appointments.csv"
df = pd.read_csv(path)
print(df.shape)
print(df.dtypes)
print(df.head())

# 1. Status counts (compare SQL Q3)
status_counts = df["status"].value_counts()
print(status_counts)

# 2. No-show rate per clinic, in percent, 2 decimals (compare SQL Q5 and Q13)
is_no_show = df["status"] == "No-Show"
print(is_no_show.head())  # Added as suggested to inspect the boolean series
no_show_rate = (is_no_show.groupby(df["clinic_id"]).mean() * 100).round(2)
print(no_show_rate)

# 3. Completed revenue per clinic (compare SQL Q4)
completed = df[df["status"] == "Completed"]
revenue = completed.groupby("clinic_id")["fee"].sum()
print(revenue)