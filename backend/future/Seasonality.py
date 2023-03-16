import json
import pandas as pd
# import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

def main():
    with open("UKI_DAI_DataEngineering_Discovery.json") as file:
        data = json.load(file)
        
    df = pd.DataFrame(data)
    df.set_index("date", inplace=True)
    df.index = pd.to_datetime(df.index)
    df = df.resample("H").mean()
    
    result = seasonal_decompose(df["value"], model="multiplicative")
    
    # plt.figure(figsize=(10, 8))
    # result.seasonal.plot()
    # plt.title("Seasonality")
    # plt.show()
    
    if result.seasonal.abs().mean() > 1:
        seasonal_data = {"date": result.seasonal.index.strftime("%Y-%m-%d %H:%M:%S").tolist(), "value": result.seasonal.values.tolist()}
        with open("seasonal_data.json", "w") as file:
            json.dump(seasonal_data, file)
        # print("Seasonality detected and saved to seasonal_data.json")
    else:
        # print("No seasonality detected")

if __name__ == '__main__':
    main()
