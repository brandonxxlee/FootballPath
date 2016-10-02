import numpy as np
import matplotlib.pyplot as plt

def plot(pairs):
    lsts = list(zip(*pairs))
    plt.plot(list(lsts[1]), list(lsts[0]), 'ro')
    plt.show()
