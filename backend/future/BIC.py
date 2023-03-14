import json
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import numpy as np

def get_p_and_q_value (past_emissions):
    # Convert the data to a DataFrame
    data = pd.DataFrame(past_emissions)

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Set date column as index
    df.set_index('date', inplace=True)

    # Set maximum p, d, q values
    max_p = 5
    max_q = 5

    # Set up BIC matrix
    BIC = np.zeros((max_p, max_q))

    # Iterate over all possible (p, q) combinations and calculate BIC
    for p in range(max_p):
        for q in range(max_q):
            try:
                model = ARIMA(df, order=(p, 1, q))
                results = model.fit()
                BIC[p, q] = results.bic
            except:
                continue

    # Find minimum BIC value and corresponding (p, q) values
    p_min, q_min = np.unravel_index(np.argmin(BIC), BIC.shape)

    # Fit model with optimal (p, q) values
    model = ARIMA(df, order=(p_min, 1, q_min))
    results = model.fit()
    
    return p_min, q_min
    
    '''
    # Print optimal (p, q) values
    print(f"Optimal (p, q) values: ({p_min}, {q_min})")

    # Plot BIC values
    fig, ax = plt.subplots()
    ax.imshow(BIC, origin='lower', cmap='Purples')
    ax.set_xlabel('q')
    ax.set_ylabel('p')
    ax.set_xticks(range(max_q))
    ax.set_yticks(range(max_p))
    ax.set_xticklabels(range(max_q))
    ax.set_yticklabels(range(max_p))
    ax.plot(q_min, p_min, 'ro')
    plt.show()
    '''
