# Create dictionary with probability mass function
import numpy as np

s1 = np.ones(4)
s2 = np.array([0,1,1,0])
t = np.array([1,0,0,1])

counts = dict()
n_samples = s1.shape[0]

# Count occurences.
for i in range(n_samples):
    if (t[i], s1[i], s2[i]) in counts.keys():
        counts[(t[i], s1[i], s2[i])] += 1
    else:
        counts[(t[i], s1[i], s2[i])] = 1

# Create PMF from counts.
pmf = dict()
for xyz, c in counts.items():
    pmf[xyz] = c / float(n_samples)
pmf