import numpy as np

c__r = 0.889972

firing_value = 1
not_firing_value = -1

#  parameters used for fig 1 and 2

# Metrics computed for each activation function
# 'H_X'
# 'I_X_R__C'
# 'I_X_C__R'
# 'I_X_R_C'
n_metrics = 4  # number of metrics to calculate

# Activation functions for the output neuron
# 'additive'
# 'modulatory'
# 'both'
# 'nocontext'
n_functions = 4  # number of activation functions

increments = 0.1
r_magnitudes = np.arange(0., 10. + increments, increments)  # The range of r magnitudes
c_magnitudes = np.arange(0., 10. + increments, increments)  # The range of c magnitudes


# fig 3

n_trials = 100
