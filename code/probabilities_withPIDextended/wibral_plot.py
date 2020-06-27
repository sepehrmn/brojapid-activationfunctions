import numpy as np
from probabilities import params
from probabilities import plotting

results = np.load("results.npy")

plotting.plot_wibral_pids(params.r_magnitudes, params.c_magnitudes, results)