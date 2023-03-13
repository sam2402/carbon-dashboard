import json
import pandas as pd
from statsmodels.tsa.stattools import adfuller

def calculate_stationarity(data):
    # Perform Dickey-Fuller test
    result = adfuller(data)
    print('ADF Statistic: {}'.format(result[0]))
    print('p-value: {}'.format(result[1]))
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t{}: {}'.format(key, value))
        
    if result[1] <= 0.05:
        print("The data is stationary")
        return True
    else:
        print("The data is not stationary")
        return False

def difference(data, interval=1):
    return [data[i] - data[i - interval] for i in range(interval, len(data))]

def main():
    with open("UKI_DAI_DataEngineering_Discovery.json") as file:
        data = json.load(file)
        
    df = pd.DataFrame(data)
    df.set_index("date", inplace=True)
    
    i = 0
    while not calculate_stationarity(df["value"]):
        i += 1
        df["value"] = difference(df["value"], interval=i)
        
    print("The number of differences required for stationarity is {}".format(i))

if __name__ == '__main__':
    main()
