import pandas as pd
from statsmodels.tsa.stattools import adfuller

def calculate_stationarity(data):
    # Perform Dickey-Fuller test
    result = adfuller(data)
    if result[1] <= 0.05:
        return True
    else:
        return False

def difference(data, interval=1):
    return [data[i] - data[i - interval] for i in range(interval, len(data))] + [data[-1]]

def get_d_value(data_list):
    df = pd.DataFrame({"value": [row["value"] for row in data_list]})
    df.index = pd.to_datetime([row["date"] for row in data_list])

    i = 0
    while not calculate_stationarity(df["value"]):
        i += 1
        df = pd.DataFrame({"value": difference(df["value"], interval=i)})
        df.index = pd.to_datetime(df.index)

    return i