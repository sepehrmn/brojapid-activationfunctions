
import numpy as np

c__r = 0.889972
corr = 0.5

# Metrics computed for each activation function
# 'H_X'
# ''
# 'I_X_R__C'
# 'I_X_C__R'
# 'I_X_R_C'
# 'shd_R_C'
# 'syn_R_C'
# 'unq_R'
# 'unq_C'
n_metrics = 8  # number of metrics to calculate

# Activation functions for the output neuron
# 'additive'
# 'modulatory'
# 'both'
# 'nocontext'
n_functions = 6  # number of activation functions

increments = 0.1
r_magnitudes = np.arange(0., 10.+increments, increments)  # The range of r magnitudes
c_magnitudes = np.arange(0., 10.+increments, increments)  # The range of c magnitudes

calculate_pid = True

firing_value = 1
not_firing_value = -1

