import json
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import timedelta
import numpy as np

# Read the JSON file
with open("carbon_emissions.json", "r") as f:
    data = json.load(f)

# Convert the JSON data to a DataFrame
df = pd.DataFrame(data)

# Check if the data columns are only 'date' and 'value', if not, select only these two columns
if set(['date', 'value']) != set(df.columns):
    df = df[['date', 'value']]

# Convert the 'date' column to date format and set it as the index
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

# Handle missing values, if encountering a blank data, use the data of the previous day to cover it
df.fillna(method='ffill', inplace=True)

# Split the dataset into training and test sets
train_data = df[-90:]
test_data = df[:-90]

# Fit the SARIMA model
model = SARIMAX(train_data, order=(2, 1, 2), seasonal_order=(1, 1, 1, 12))

# Train the SARIMA model
model_fit = model.fit()

# Print the model summary information
print(model_fit.summary())

# Generate the model residuals
residuals = model_fit.resid

# Plot the histogram of residuals
plt.hist(residuals)
plt.title("Residuals Histogram")
plt.show()

# Predict the future 3 months data
predictions = model_fit.forecast(steps=90)

# Create the prediction result DataFrame
pred_df = pd.DataFrame({'date': [], 'value': []})
date = df.index[-1]
for i in range(90):
    date += timedelta(days=1)
    pred_df = pred_df.append({'date': date.strftime("%Y-%m-%d"), 'value': predictions[i]}, ignore_index=True)

# Write the prediction result to the JSON file
with open("predicted_carbon_emissions.json", "w") as f:
    json.dump(pred_df.to_dict(orient='records'), f)

# Calculate the RMSE
predictions_df = pd.DataFrame(predictions, columns=['value'], index=test_data.index)
rmse = np.sqrt(np.mean((predictions_df['value'] - test_data['value'])**2))
print("RMSE: ", rmse)
