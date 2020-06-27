
import numpy as np

n_trials = 1 * pow(10, 3)

# Metrics computed for each activation function
# 'mi_X_R_conC'
# 'mi_X_C_conR'
# 'mi_X_R_C'
# 'shd_R_C'
# 'syn_R_C'
# 'unq_R'
# 'unq_C'
n_metrics = 7  # number of metrics to calculate

# Activation functions for the output neuron
# 'additive'
# 'modulatory'
# 'both'
# 'nocontext'
n_functions = 4  # number of activation functions

increments = 0.25
r_magnitudes = np.arange(0., 10.+increments, increments)  # The range of r magnitudes
c_magnitudes = np.arange(0., 10.+increments, increments)  # The range of c magnitudes
