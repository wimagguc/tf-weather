import numpy as np
import pandas as pd
import matplotlib

# For the plots to work on MacOSX.
# Has to be before the plt import, no matter what flake8 says.
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Import data
    data = pd.read_csv('data/LND_weather_data.csv')

    # Drop unused variables
    data = data.drop(['station_id'], 1)
    data = data.drop(['station_name'], 1)
    data = data.drop(['almanac_dt'], 1)
    data = data.drop(['record_hi'], 1)
    data = data.drop(['record_hi_yr'], 1)
    data = data.drop(['record_lo'], 1)
    data = data.drop(['record_lo_yr'], 1)
    data = data.drop(['mean_temp'], 1)
    data = data.drop(['avg_precip'], 1)
    data = data.drop(['avg_snow'], 1)
    data = data.drop(['record_period'], 1)

    # Make data a numpy array
    data = data.values

    # Dimensions of dataset: number of rows (n)
    n = data.shape[0]

    # Create training and test data sets
    train_start = 0
    train_end = int(np.floor(0.8 * n))
    test_start = train_end
    test_end = n
    data_train = data[np.arange(train_start, train_end), :]
    data_test = data[np.arange(test_start, test_end), :]

    # Plot the training data
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(data_train)
    ax1.plot(data_test)
    plt.show()
