import pandas as pd
import matplotlib.pyplot as plt

class chaepy:

    @staticmethod
    def read_csv(data_file):
        return pd.read_csv(data_file)

    @staticmethod
    def plot(data, x_column, y_column):
        plt.plot(data[x_column], data[y_column])
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.show()

