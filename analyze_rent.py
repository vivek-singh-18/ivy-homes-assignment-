import json
import pandas as pd

with open("v1_rentals.json") as f:
    rentals = json.load(f)

df = pd.DataFrame(rentals)
kukatpally_rentals = df[df["locality"].str.lower() == "kukatpally"]
total_monthly_rent = kukatpally_rentals["price"].sum()
print("Q5. total_monthly_rent:", total_monthly_rent)

