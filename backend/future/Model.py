import pandas as pd
# import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime, timezone

from statsmodels.graphics.gofplots import qqplot 

def calculate_step(past_data, future_date: datetime):
    # Convert the 'date' column to datetime format
    past_data_dates = [data['date'].replace(tzinfo=timezone.utc) for data in past_data]
    # past_data_dates = [data['date'] for da ta in past_data]

    # Get the time difference between the last two dates
    time_delta = past_data_dates[-1] - past_data_dates[-2]

    # Calculate the step
    step = int((future_date.replace(tzinfo=timezone.utc) - past_data_dates[-1]).total_seconds() / time_delta.total_seconds())

    return step
    
def get_future_emissions(past_emissions, future_date: datetime):
    # Convert the data to a DataFrame
    df = pd.DataFrame(past_emissions)

    # Convert the 'date' column to date format and set it as the index
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    
    # Split the dataset into training and test sets
    train_data = df[-360:]
    test_data = df[:-360]
    
    #use Dickey-Fuller test to calculate the differencing
    from .differencing import get_d_value
    d = get_d_value(past_emissions)
    
    #use BIC to calculate the p and q value
    from .BIC import get_p_and_q_value
    a, b = get_p_and_q_value(past_emissions, d)
    
    # set the order for SARIMA
    p = a
    d = d
    q = b
    P = 0
    D = 0
    Q = 0
    m = 0
    
    # Fit the SARIMA model
    model = SARIMAX(train_data, order=(p, d, q), seasonal_order=(P, D, Q, m))
    
    # Train the SARIMA model
    model_fit = model.fit()
    
    # Print the model summary information
    # print(model_fit.summary())

    # Generate the model residuals
    residuals = model_fit.resid

    # Plot the histogram of residuals, check the accuracy by histogram of residuals
    # plt.hist(residuals)
    # plt.title("Residuals Histogram")
    # plt.xlabel("Residual Value")
    # plt.ylabel("Frequency")  # add y-axis
    # plt.show()
    
    # Plot the QQ plot of residuals  
    # Using the 's' parameter to draw a reference line means drawing a line with a slope of 1 and an intercept of 0
    # qqplot(residuals, line='s')
    # plt.title("Residuals QQ Plot")
    # plt.show()

    # Get the number of steps to predict
    step = calculate_step(past_emissions, future_date)

    # Predict the future data
    predictions = model_fit.forecast(steps=step)
    predict_time = predictions.index
    
    # Create the prediction result list
    pred_list_dic = []
    for i in range(step):
        date = predict_time[i].replace(second=0, microsecond=0)
        pred_list_dic.append({'date': date, 'value': predictions[i]})

    return pred_list_dic
