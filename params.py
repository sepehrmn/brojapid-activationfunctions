import numpy as np

c__r = 0.889972

firing_value = 1
not_firing_value = -1

# Activation functions for the output neuron
# 'additive'
# 'modulatory'
# 'both'
# 'nocontext'
n_functions = 4  # number of activation functions

increments = 0.1
r_magnitudes = np.arange(0., 10. + increments, increments)  # The range of r magnitudes
c_magnitudes = np.arange(0., 10. + increments, increments)  # The range of c magnitudes
