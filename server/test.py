import matplotlib.pyplot as plt
import numpy as np

from gardener import Gardener


def plot_fogging_function(begin, end, step):
    x = list(np.arange(begin, end, step))
    y = list(Gardener.compute_fogging_period(xx) for xx in x)
    table = list((str(xx), str(Gardener.compute_fogging_period(xx))) for xx in list(range(0, 35, 5)))

    plt.plot(x, y)
    plt.title('Fogging interval depends on current temperature')
    plt.xlabel('temperature (°C)')
    plt.ylabel('fogging interval (minutes)')
    plt.table(cellText=table, cellLoc='center', loc='bottom', bbox=[0.45, 0.45, 0.3, 0.4])
    plt.show()


def plot_watering_function(begin, end, step):
    x = list(np.arange(begin, end, step))
    y = list(Gardener.compute_watering_period(xx) for xx in x)
    table = list((str(xx), str(Gardener.compute_watering_period(xx))) for xx in list(range(0, 35, 5)))

    plt.plot(x, y)
    plt.title('Watering interval depends on current temperature')
    plt.xlabel('temperature (°C)')
    plt.ylabel('watering interval (minutes)')
    plt.table(cellText=table, cellLoc='center', loc='bottom', bbox=[0.45, 0.45, 0.3, 0.4])
    plt.show()


plot_watering_function(begin=0, end=30, step=0.1)
plot_fogging_function(begin=0, end=30, step=0.1)
