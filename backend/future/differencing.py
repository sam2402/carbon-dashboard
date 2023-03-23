import pandas as pd
from statsmodels.tsa.stattools import adfuller

def calculate_stationarity(data):
    """
    Check if the given time series data is stationary with the Augmented Dickey-Fuller test.
    
    Args:
        data(pd.Series): The input time series data.
    
    Return: 
        bool: True if the data is stationary, False otherwise.
    """
    # Perform Dickey-Fuller test
    result = adfuller(data)
    if result[1] <= 0.05:
        return True
    else:
        return False

def difference(data, interval=1):
    """
    Calculates the difference between elements in the time series data with a given interval.
    
    Args:
        data(pd.Series): The input time series data
        interval(int): The interval to use when calculating differences, defaults to 1 in our case
    
    Return: 
        list: The list of differences for the input data
    """
    return [data[i] - data[i - interval] for i in range(interval, len(data))] + [data[-1]]

def get_d_value(data_list):
    """
    Determines the order of differencing (d) by checking the time series data stationarity.
    
    Args:
        data_list(list): A list of dictionaries with "date" and "value" keys representing the time series data
    
    Return: 
        int: The optimal order of differencing (d).
    """
    df = pd.DataFrame({"value": [row["value"] for row in data_list]})
    df.index = pd.to_datetime([row["date"] for row in data_list])

    i = 0
    while not calculate_stationarity(df["value"]):
        i += 1
        df = pd.DataFrame({"value": difference(df["value"], interval=i)})
        df.index = pd.to_datetime(df.index)

    return i