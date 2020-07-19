import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def _plot_subplot(label, metric, number, function, results):
    """Plot a subplot for figure 2.

    :param label: string - label of the subplot
    :param metric: string - information metric
    :param number: int - number of the subplot
    :param function: string - activation function
    :param results: structured array - results of the analysis
    :return: None
    """
    ax = plt.subplot(3, 1, number, projection='3d')
    ax.set_xlabel('r', labelpad=15, fontsize=22)
    ax.set_ylabel('c', labelpad=15, fontsize=22)
    ax.xaxis.set_tick_params(labelsize=11)
    ax.yaxis.set_tick_params(labelsize=11)
    ax.zaxis.set_tick_params(labelsize=11, pad=6)
    ax.set_zlabel('Information bits', labelpad=15, fontsize=18)
    matches = results[np.where(np.logical_and( results['information_metric']
                                         == metric, results['activation_function'] == function))]
    X = matches['r'].reshape(101, 101)
    Y = matches['c'].reshape(101, 101)
    Z = matches['value'].reshape(101, 101)

    ax.set_title(label, fontsize=19, fontweight='bold', y=0.1, x=0.1)
    ax.plot_wireframe(X, Y, Z, color="grey")
    ax.view_init(45, 300)
    plt.tight_layout()

    return


def plot_surfaceplots(results):
    """Plot figure 2. Calls "_plot_fig2_subplot"

    :param results: structured array - results of the analysis
    :return: None
    """
    plt.figure(figsize=(9, 10.8))

    _plot_subplot("(a)", 'I_X_C__R', 1, 'additive', results)
    _plot_subplot("(b)", 'I_X_C__R', 2, 'modulatory', results)
    _plot_subplot("(c)", 'I_X_C__R', 3, 'both', results)

    plt.subplots_adjust(wspace=None, hspace=0.2)
    plt.show()

    return


