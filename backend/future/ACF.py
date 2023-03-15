import json
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Read data from JSON file
with open('diff_data.json', 'r') as f:
    data = json.load(f)

# Convert data to DataFrame
df = pd.DataFrame(data)

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Set date column as index
df.set_index('date', inplace=True)

# Calculate autocorrelation
acf = sm.graphics.tsa.plot_acf(df['value'], lags=30)

# Add y-axis label
plt.ylabel("Autocorrelation")

# Show plot
plt.show()
