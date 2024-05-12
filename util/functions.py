import numpy as np
import matplotlib.pyplot as plt

def plot(xVector, yVector, xLabel, yLabel, title, scale=None):
    plt.plot(xVector, yVector)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.xscale(scale) if scale is not None else None
    plt.title(title)
    plt.grid(True)
    plt.show()
