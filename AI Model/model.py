import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.callbacks import EarlyStopping

# Read data
with open('monthly_sine_carbon_emissions.json', 'r') as f:
    data = json.load(f)

# Extract data
df = pd.DataFrame(data)
df = df[['date', 'value']]

# Convert date column to timestamp
df['date'] = pd.to_datetime(df['date'])

# Set timestamp as index
df.set_index('date', inplace=True)

# Interpolate missing data
df = df.interpolate()

# Normalize data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df)

# Define function to create training data
def create_train_data(dataset, look_back=1):
    X, Y = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i+look_back), 0]
        X.append(a)
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)

# Create training data
look_back = 90
train_data = scaled_data[:-90]
X_train, Y_train = create_train_data(train_data, look_back)

# Reshape input data to 3D
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Create LSTM model
model = Sequential()
model.add(LSTM(units=128, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(units=128, return_sequences=True))
model.add(LSTM(units=128))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Set up early stopping
early_stop = EarlyStopping(monitor='val_loss', patience=10)

# Train model
model.fit(X_train, Y_train, epochs=150, batch_size=64, validation_split=0.1, callbacks=[early_stop])

# Predict daily data for next 3 months
last_date = df.index[-1]
prediction_dates = pd.date_range(last_date, periods=90, freq='D')
prediction_data = np.empty((90, 1))
prediction_data[0:look_back] = scaled_data[-look_back:]

for i in range(look_back, 90):
    x_input = prediction_data[(i-look_back):i, 0]
    x_input = np.reshape(x_input, (1, look_back, 1))
    yhat = model.predict(x_input)
    prediction_data[i] = yhat

# Inverse normalization
prediction_data = scaler.inverse_transform(prediction_data)

# Generate dates and values for predictions
predictions = pd.DataFrame(prediction_data, index=prediction_dates, columns=['value'])

# Calculate Root Mean Square Error
train = df.iloc[:-90]
test = df.iloc[-90:]
test['predictions'] = predictions[:90]
rmse = np.sqrt(np.mean((test['value'] - test['predictions'])**2))
print('RMSE:', rmse)

# Generate new JSON file to store data
predictions.reset_index(inplace=True)
predictions.rename(columns={'index': 'date'}, inplace=True)
predictions['date'] = predictions['date'].dt.strftime('%Y-%m-%d')
predictions_json = predictions.to_dict('records')

with open('co2_emissions_predictions.json', 'w') as f:
    json.dump(predictions_json, f)
