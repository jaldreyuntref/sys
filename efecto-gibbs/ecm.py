import numpy as np

def calculateECM(original, reconstructed):
    return np.mean((original - reconstructed) ** 2)