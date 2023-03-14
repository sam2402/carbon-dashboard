import json
import pandas as pd

# Read data from JSON file
with open('carbon_emissions.json', 'r') as f:
    data = json.load(f)

# Convert data to DataFrame
df = pd.DataFrame(data)

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Set date column as index
df.set_index('date', inplace=True)

# Calculate difference between consecutive values
df_diff = df.diff()

# Drop first row since it will be NaN
df_diff.dropna(inplace=True)

# Convert DataFrame to list of dictionaries with str type dates
diff_data = df_diff.reset_index().to_dict('records')
for d in diff_data:
    d['date'] = str(d['date'])

# Save diff data to JSON file
with open('diff_data.json', 'w') as f:
    json.dump(diff_data, f)

# Plot diff data
df_diff.plot()
