from hilbertTransform import hilbertTransform 
from movingAverageFilter import movingAverageFilter

def smoothingFilter(signal, L):
    signal = hilbertTransform(signal)
    return movingAverageFilter(signal, L)