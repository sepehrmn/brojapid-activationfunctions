import itertools
import math
import random

import analysis
import numpy as np
import params
import plotting

from simulations import generation

#import mpi4py

if __name__ == '__main__':

    additive_array = np.zeros(params.n_trials, dtype=np.int)
    modulatory_array = np.zeros(params.n_trials, dtype=np.int)
    both_array = np.zeros(params.n_trials, dtype=np.int)
    nocontext_array = np.zeros(params.n_trials, dtype=np.int)

    results_n = params.r_magnitudes.shape[0] * params.c_magnitudes.shape[0] * params.n_metrics * params.n_functions  # number of results
    # This is a coarse grid search so it is ok to, for convenience, put everything in one big structured array
    results = np.zeros(results_n, dtype=[('activation_function', 'S40'),
                                         ('information_metric', 'S40'),
                                         ('r', np.float),
                                         ('c', np.float),
                                         ('value', np.float)])
    # Simulation
    # looping over r and c magnitudes:
    idx = 0
    for rmag, cmag in itertools.product(params.r_magnitudes, params.c_magnitudes):

        r_firing = +1 * rmag
        r_silent = -1 * rmag

        c_firing = +1
        c_silent = -1
        # Create R and C
        random.seed(135)
        R, C = generation.gen_input(params.n_trials, r_firing, r_silent, c_firing, c_silent)

        # Simulating over the trials
        for sampnum in range(params.n_trials):

            # Random number
            rn = random.random()

            # Activation function 1: additive
            additive = R[sampnum] + C[sampnum]
            #additive_p = 1 / (1 + math.exp(-additive))
            additive = np.array([additive], dtype=np.float128)
            additive_p = 1 / (1 + np.exp(-additive)[0])
            #
            additive_array[sampnum] = +1 if additive_p >= rn else 0

            # Activation function 2: Modulatory
            modulatory = 0.5 * R[sampnum] * (1 + math.exp(R[sampnum] * C[sampnum]))
            #modulatory_p = 1 / (1 + math.exp(-modulatory))
            modulatory = np.array([modulatory], dtype=np.float128)
            #modulatory_p = 1 / (1 + np.exp(-modulatory)[0])
            #

            modulatory_array[sampnum] = +1 if (1 / (1 + np.exp(-modulatory)[0])) >= rn else 0

            # Activation function 3: Additive and Modulatory
            both = 0.5 * R[sampnum] * (1 + math.exp(R[sampnum] * C[sampnum])) + C[sampnum]
            #both_p = 1 / (1 + math.exp(-both))

            both = np.array([both], dtype=np.float128)
            #both_p = 1.0 / (1 + np.exp(-both))
            #
            both_array[sampnum] = +1 if (1.0 / (1 + np.exp(-both))) >= rn else 0

            # Activation function 4: No Context

            nocontext = R[sampnum]
            nocontext_p = 1 / (1 + math.exp(-nocontext))
            nocontext_array[sampnum] = +1 if nocontext_p >= rn else 0

        # A spike is encoded by (1 * magnitude), and no spike by 0
        # Transforming all values to 0 and 1 due to JIDT requirements

        transformed_R = np.zeros(params.n_trials, dtype=np.int)  # creating array of 0
        np.put(transformed_R, np.where(R != r_silent), 1)  # transforming the firing magnitude to 1

        transformed_C = np.zeros(params.n_trials, dtype=np.int)  # creating array of 0
        np.put(transformed_C, np.where(C != c_silent), 1)  # transforming the firing magnitude to 1

        # Calculating the MIs and PID
        spikes = {'additive': additive_array, 'modulatory': modulatory_array, 'both': both_array,
                   'nocontext': nocontext_array}

        functions_metrics = analysis.calculate_metrics(transformed_R, transformed_C, spikes, True)
        for function, metrics in functions_metrics.items():
            for metric, value in metrics.items():
                results[idx] = (function, metric, rmag, cmag, value)
                idx += 1

    plotting.plot_fig1(params.r_magnitudes, results)
    #plotting.plot_fig2(params.r_magnitudes, params.c_magnitudes, results)
    #plotting.plot_pids(r_magnitudes, c_magnitudes, results)


