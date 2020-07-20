import itertools
import numpy as np
from scipy.special import expit
import params
import analysis
import plotting


# P(X)
def cal_X(R, C, RCX):

    X = {0: 0, 1: 0}
    for x, r, c in itertools.product(X, R, C):
                X[x] += RCX[(r, c, x)]
    return X


# P(R|C)
def cal_R__C(R, C, RC):

    R__C = {}
    for c, r in itertools.product(C, R):
        if np.isclose(C[c], 0.0):
            R__C[(r, c)] = 0.0
        else:
            R__C[(r, c)] = RC[(r, c)] / C[c]
    return R__C


# P(C|R)
def cal_C__R(R, C, RC):

    C__R = {}
    for r, c in itertools.product(R, C):
            if np.isclose(R[r], 0.0):
                C__R[(c, r)] = 0.0
            else:
                C__R[(c, r)] = RC[(r, c)] / R[r]
    return C__R

# P(X|R)
def cal_X__R(R, X, RCX):
    XR = {}
    for x, r in itertools.product(X, R):
        XR[(x, r)] = RCX[(r, 0, x)] + RCX[(r, 1, x)]

    X__R = {}
    for x, r in itertools.product(X, R):
        if np.isclose(R[r], 0.0):
            X__R[(x, r)] = 0.0
        else:
            X__R[(x, r)] = XR[(x, r)] / R[r]

    return X__R


# P(X|C)
def cal_X__C(C, X, RCX):
    XC = {}
    for x, c in itertools.product(X, C):
        XC[(x, c)] = RCX[(0, c, x)] + RCX[(1, c, x)]

    X__C = {}
    for x, c in itertools.product(X, C):
        if np.isclose(C[c], 0.0):
            X__C[(x, c)] = 0.0
        else:
            X__C[(x, c)] = XC[(x, c)] / C[c]

    return X__C


if __name__ == '__main__':

    # Setting the seed.
    np.random.seed(77)

    # number of results
    n_results = params.r_magnitudes.shape[0] * params.c_magnitudes.shape[0] * params.n_metrics * params.n_functions
    # It is OK to for convenience put everything in one big structured array
    analytical_results = np.zeros(n_results, dtype=[('activation_function', 'O'),
                                         ('information_metric', 'O'),
                                         ('r', np.float),
                                         ('c', np.float),
                                         ('value', np.float)])

    # Creating the input probability distributions based on equations 1-4 in the replication.
    r_c = 0.5 * params.c__r
    r_notc = 0.5 * (1 - params.c__r)
    notr_c = 0.5 * (1 - params.c__r)
    notr_notc = 0.5 * params.c__r

    R = {0: notr_c + notr_notc, 1: r_c + r_notc}
    C = {0: r_notc + notr_notc, 1: r_c + notr_c}

    RC = {(0, 0): notr_notc, (0, 1): notr_c, (1, 0): r_notc, (1, 1): r_c}
    R__C = cal_R__C(R, C, RC)
    C__R = cal_C__R(R, C, RC)

    # looping over r and c magnitudes and calculating the result of each activation function in equations 5-7 of
    # the replication. The result of each activation function is passed into the sigmoidal in equation 8.
    idx = 0
    for rmag, cmag in itertools.product(params.r_magnitudes, params.c_magnitudes):

        spiking_r = {0: params.not_firing_value * rmag, 1: params.firing_value * rmag}
        spiking_c = {0: params.not_firing_value * cmag, 1: params.firing_value * cmag}

        # Activation function 1: additive
        additive_X__R_C = {}
        for r, val_rspike in spiking_r.items():
            for c, val_cspike in spiking_c.items():

                val_additive = val_rspike + val_cspike
                additive_firing = expit(val_additive)
                additive_silent = 1 - additive_firing
                additive_X__R_C[(1, r, c)] = additive_firing
                additive_X__R_C[(0, r, c)] = additive_silent

        # Activation function 2: modulatory
        modulatory_X__R_C = {}
        for r, val_rspike in spiking_r.items():
            for c, val_cspike in spiking_c.items():

                vals_modulatory = 0.5 * val_rspike * (1 + np.exp(val_rspike * val_cspike))
                modulatory_firing = expit(vals_modulatory)
                modulatory_silent = 1 - modulatory_firing
                modulatory_X__R_C[(1, r, c)] = modulatory_firing
                modulatory_X__R_C[(0, r, c)] = modulatory_silent

        # Activation function 3: additive and modulatory
        both_X__R_C = {}
        for r, val_rspike in spiking_r.items():
            for c, val_cspike in spiking_c.items():

                vals_both = 0.5 * val_rspike * (1 + np.exp(val_rspike * val_cspike)) + val_cspike
                both_firing = expit(vals_both)
                both_silent = 1 - both_firing
                both_X__R_C[(1, r, c)] = both_firing
                both_X__R_C[(0, r, c)] = both_silent

        # Activation function 4: No Context
        nocontext_X__R_C = {}
        for r, val_rspike in spiking_r.items():
            for c, val_cspike in spiking_c.items():

                vals_nocontext = val_rspike
                nocontext_firing = expit(vals_nocontext)
                nocontext_silent = 1 - nocontext_firing
                nocontext_X__R_C[(1, r, c)] = nocontext_firing
                nocontext_X__R_C[(0, r, c)] = nocontext_silent

        # Generating probability distributions

        # P(x|r,c)
        functions_X__R_C = {'additive': additive_X__R_C,
                            'modulatory': modulatory_X__R_C,
                            'both': both_X__R_C,
                            'nocontext': nocontext_X__R_C}

        functions_RCX = {}  # P(R,C,X)
        functions_X = {}  # P(X)
        functions_X__R = {}  # P(X|R)
        functions_X__C = {}  # P(X|C)

        for function, X__R_C in functions_X__R_C.items():

            # P(R,C,X)
            X = {0: 0, 1: 0}
            RCX = {}
            for x, c, r in itertools.product(X, C, R):
                RCX[(r, c, x)] = RC[(r, c)] * X__R_C[(x, r, c)]
            functions_RCX[function] = RCX

            # P(X)
            X = cal_X(R, C, RCX)
            functions_X[function] = cal_X(R, C, RCX)

            # P(X|R)
            functions_X__R[function] = cal_X__R(R, X, RCX)

            # P(X|C)
            functions_X__C[function] = cal_X__C(C, X, RCX)

        # Calculating information theoretic metrics
        functions_metrics = analysis.cal_fun_met(R, C, functions_X, functions_X__R, functions_X__C,
                                                       functions_X__R_C, functions_RCX)

        for function, metrics in functions_metrics.items():
           for metric, value in metrics.items():
               analytical_results[idx] = (function, metric, rmag, cmag, value)
               idx += 1

    plotting.plot_surfaceplots(analytical_results)

