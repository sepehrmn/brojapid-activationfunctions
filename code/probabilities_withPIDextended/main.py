import itertools
import math
import random
import numpy as np

from probabilities_withPIDextended import params
from probabilities_withPIDextended import analysis
from probabilities_withPIDextended import plotting


if __name__ == '__main__':

    #np.seterr(all='warn', over='raise')

    # number of results
    n_results = params.r_magnitudes.shape[0] * params.c_magnitudes.shape[0] * params.n_metrics * params.n_functions
    # It is OK to for convenience, put everything in one big structured array
    results = np.zeros(n_results, dtype=[('activation_function', 'S40'),
                                         ('information_metric', 'S40'),
                                         ('r', np.float),
                                         ('c', np.float),
                                         ('value', np.float)])

    # r_c, r_notc, notr_c, notr_not
    r_c = params.corr * params.c__r
    r_notc = params.corr * (1 - params.c__r)
    notr_c = params.corr * (1 - params.c__r)
    notr_notc = params.corr * params.c__r

    r = {0: notr_c + notr_notc, 1: r_c + r_notc}
    c = {0: r_notc + notr_notc, 1: r_c + notr_c}

    rc = {(0, 0): notr_notc, (0, 1): notr_c, (1, 0): r_notc, (1, 1): r_c}

    # P(r|c)
    r__c = {}
    for letter_c, letter_r in itertools.product(c,r):
            r__c[(letter_r, letter_c)] = rc[(letter_r, letter_c)] / c[letter_c]

    # P(c|r)
    c__r = {}
    for letter_r, letter_c in itertools.product(r,c):
            c__r[(letter_c, letter_r)] = rc[(letter_r, letter_c)] / r[letter_r]


    # looping over r and c magnitudes:
    idx = 0
    for rmag, cmag in itertools.product(params.r_magnitudes, params.c_magnitudes):

        # try:
        spiking_r = {0: params.not_firing_value * rmag, 1: params.firing_value * rmag}
        spiking_c = {0: params.not_firing_value * cmag, 1: params.firing_value * cmag}

        # Activation function 1: additive
        additive_x__r_c = {}
        for letter_rspike, val_rspike in spiking_r.items():
            for letter_cspike, val_cspike in spiking_c.items():

                val_additive = val_rspike + val_cspike
                additive_firing = 1 / (1 + np.exp(-val_additive))
                additive_silent = 1 - additive_firing
                additive_x__r_c[(1, letter_rspike, letter_cspike)] = additive_firing
                additive_x__r_c[(0, letter_rspike, letter_cspike)] = additive_silent

        # Activation function 2: modulatory
        modulatory_x__r_c = {}
        for letter_rspike, val_rspike in spiking_r.items():
            for letter_cspike, val_cspike in spiking_c.items():

                #vals_modulatory = np.zeros(1,dtype=np.float128)
                vals_modulatory = 0.5 * val_rspike * (1 + np.exp(2* val_rspike * val_cspike))
                vals_modulatory = np.exp(-vals_modulatory)
                modulatory_firing = 1. / (1. + vals_modulatory)
                modulatory_silent = 1 - modulatory_firing + 0.000001
                modulatory_x__r_c[(1, letter_rspike, letter_cspike)] = modulatory_firing
                modulatory_x__r_c[(0, letter_rspike, letter_cspike)] = modulatory_silent

        # Activation function 3: additive and modulatory
        both_x__r_c = {}
        for letter_rspike, val_rspike in spiking_r.items():
            for letter_cspike, val_cspike in spiking_c.items():

                vals_both = 0.5 * val_rspike * (1 + math.exp(val_rspike * val_cspike)) + val_cspike
                both_firing = 1.0 / (1 + np.exp(-vals_both))
                both_silent = 1 - both_firing
                both_x__r_c[(1, letter_rspike, letter_cspike)] = both_firing
                both_x__r_c[(0, letter_rspike, letter_cspike)] = both_silent

        # Activation function 4: No Context
        nocontext_x__r_c = {}
        for letter_rspike, val_rspike in spiking_r.items():
            for letter_cspike, val_cspike in spiking_c.items():

                vals_nocontext = val_rspike
                nocontext_firing = 1 / (1 + np.exp(-vals_nocontext))
                nocontext_silent = 1 - nocontext_firing
                nocontext_x__r_c[(1, letter_rspike, letter_cspike)] = nocontext_firing
                nocontext_x__r_c[(0, letter_rspike, letter_cspike)] = nocontext_silent

        # Activation function 5: alternative modulatory function proposed by Nikolaus Kriegeskorte
        amod_x__r_c = {}
        for letter_rspike, val_rspike in spiking_r.items():
            for letter_cspike, val_cspike in spiking_c.items():

                #vals_modulatory = np.zeros(1,dtype=np.float128)
                vals_amod = val_rspike * (1 + val_cspike)
                amod_firing = 1. / (1. + np.exp(-vals_amod))
                amod_silent = 1 - amod_firing + 0.000001
                amod_x__r_c[(1, letter_rspike, letter_cspike)] = amod_firing
                amod_x__r_c[(0, letter_rspike, letter_cspike)] = amod_silent

        # Activation function 6: linear rectifier function proposed by Nikolaus Kriegeskorte
        max_x__r_c = {}
        for letter_rspike, val_rspike in spiking_r.items():
            for letter_cspike, val_cspike in spiking_c.items():

                #vals_modulatory = np.zeros(1,dtype=np.float128)
                vals_max = np.maximum(0, 2 * val_rspike + val_cspike - 1)
                max_firing = 1. / (1. + np.exp(-vals_max))
                max_silent = 1 - max_firing + 0.000001
                max_x__r_c[(1, letter_rspike, letter_cspike)] = max_firing
                max_x__r_c[(0, letter_rspike, letter_cspike)] = max_silent

        # Generating probability distributions

        # P(x,r,c)
        functions_x__r_c = {'additive': additive_x__r_c, 'modulatory': modulatory_x__r_c, 'both': both_x__r_c,
                   'nocontext': nocontext_x__r_c, 'amod':amod_x__r_c, 'max':max_x__r_c}

        functions_x = {}  # P(x)
        functions_x__r = {} # P(x|r)
        functions_x__c = {} # P(x|c)

        functions_rcx = {}
        for function, x__r_c in functions_x__r_c.items():

            x = {0: 0, 1: 0}
            # P(r,c,x)
            rcx = {}
            for letter_x, letter_c, letter_r in itertools.product(x, c, r):
                        rcx[(letter_r, letter_c, letter_x)] = rc[(letter_r, letter_c)] * x__r_c[(letter_x, letter_r, letter_c)]
            functions_rcx[function] = rcx

            # P(x|r)
            xr = {}
            for letter_x, letter_r in itertools.product(x, r):
                        xr[(letter_x, letter_r)] = rcx[(letter_r, 0, letter_x)] + rcx[(letter_r, 1, letter_x)]

            x__r = {}
            for letter_x, letter_r in itertools.product(x, r):
                        x__r[(letter_x, letter_r)] = xr[(letter_x, letter_r)] / r[(letter_r)]

            functions_x__r[function] = x__r

            # P(x|c)
            xc = {}
            for letter_x, letter_c in itertools.product(x, c):
                        xc[(letter_x, letter_c)] = rcx[(0, letter_c, letter_x)] + rcx[(1, letter_c, letter_x)]

            x__c = {}
            for letter_x, letter_c in itertools.product(x, c):
                        x__c[(letter_x, letter_c)] = xc[(letter_x, letter_c)] / c[(letter_c)]
            functions_x__c[function] = x__c

            # P(x)
            for letter_x, letter_r, letter_c in itertools.product(x, r, c):
                        x[letter_x] += rcx[(letter_r, letter_c, letter_x)]
            functions_x[function] = x

            # for letter_x, letter_r, letter_c in itertools.product(x,r,c):
            #             x[letter_x] += x__r_c[(letter_x, letter_r, letter_c)] * r__c[(letter_r, letter_c)]
            # functions_x[function] = x

        # Calculating information theoretic metrics
        functions_metrics = analysis.calculate_metrics(r, c, functions_x, functions_x__r, functions_x__c,
                                                       functions_x__r_c, functions_rcx, params.calculate_pid)

        for function, metrics in functions_metrics.items():
           for metric, value in metrics.items():
               results[idx] = (function, metric, rmag, cmag, value)
               idx += 1

    np.save("results.npy", results)

    plotting.plot_fig1(params.r_magnitudes, results)
    plotting.plot_MIs(params.r_magnitudes, params.c_magnitudes, results)
    plotting.plot_pids(params.r_magnitudes, params.c_magnitudes, results)
    #plotting.plot_wibral_pids(params.r_magnitudes, params.c_magnitudes, results)
    #plotting.plot_spectra(a, b, results)
