import pandas as pd

df = pd.read_csv(
    "/mnt/c/Users/Nikhil_Chamle/Desktop/banking_data/day_1/loan_master.csv"
)

df.to_csv(
    "/mnt/c/Users/Nikhil_Chamle/Desktop/banking_data/day_1/loan_master_fixed.csv",
    sep="|",
    index=False
)

print("Done")