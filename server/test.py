import matplotlib.pyplot as plt
import numpy as np


def plot_watering_function(begin, end, step):
    x = list(np.arange(begin, end, step))
    y = list(24*60/(xx-4)**1.5 for xx in x)
    table = list((str(xx),str(round(24*60/(xx-4)**1.5))) for xx in [5, 10, 20, 30, 40])

    plt.plot(x, y)
    plt.title('Watering interval depends on current temperature')
    plt.legend(['24*60/(t-4)**1.5'])
    plt.xlabel('temperature (°C)')
    plt.ylabel('watering interval (minutes)')
    plt.table(cellText=table, cellLoc='center', loc='bottom', bbox=[0.65, 0.45, 0.3, 0.4])
    plt.show()


def plot_fogging_function(begin, end, step):
    x = list(np.arange(begin, end, step))
    y = list(24*60/(xx-4)**2 for xx in x)
    table = list((str(xx),str(round(24*60/(xx-4)**2))) for xx in [5, 10, 20, 30, 40])

    plt.plot(x, y)
    plt.title('Fogging interval depends on current temperature')
    plt.legend(['24*60/(t-4)**2'])
    plt.xlabel('temperature (°C)')
    plt.ylabel('fogging interval (minutes)')
    plt.table(cellText=table, cellLoc='center', loc='bottom', bbox=[0.65, 0.45, 0.3, 0.4])
    plt.show()


plot_watering_function(begin=4.1, end=50, step=0.1)
plot_fogging_function(begin=4.1, end=50, step=0.1)

