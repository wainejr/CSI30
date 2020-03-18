import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    """[summary]
    Implement Ian
    """
    def __init__(self):
        pass

    def plot_histogram(self, interval_dict):
        pass

    def plot_line(self, x, y):
        plt.plot(x, y)
        pass

    def plot_points(self, x, y):
        plt.scatter(x, y)

    def flush(self):
        plt.gca().clear()
        pass

    def save_plots(self, x_name, y_name, img_filename, plot_name):
        plt.xlabel(x_name)
        plt.ylabel(y_name)
        plt.title(plot_name)
        plt.savefig('images/' + img_filename + '.png')
        plt.gca().clear()
