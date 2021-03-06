import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def _plot_subplot(label, metric, total_number, number, function, results):
    """Plot a subplot.

    :param label: string - label of the subplot
    :param metric: string - information metric
    :param total_number: int - total number of columns (subplots) for the plot
    :param number: int - number of the subplot
    :param function: string - activation function
    :param results: structured array - results of the analysis
    :return: None
    """
    ax = plt.subplot(1, total_number, number, projection='3d')
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


def plot_classical_surfaceplots(results):
    """Plot surface plots. Calls "_plot_subplot"

    :param results: structured array - results of the analysis
    :return: None
    """
    plt.figure(figsize=(25, 11))

    _plot_subplot("(a)", 'I_X_C__R', 3, 1, 'additive', results)
    _plot_subplot("(b)", 'I_X_C__R', 3, 2, 'modulatory', results)
    _plot_subplot("(c)", 'I_X_C__R', 3, 3, 'both', results)

    plt.subplots_adjust(wspace=None, hspace=0.2)
    plt.savefig("classical_terms.png")

    return

def plot_pid_surfaceplots(results, activation_function):
    """Plot surface plots. Calls "_plot_subplot"

    :param results: structured array - results of the analysis
    :return: None
    """
    plt.figure(figsize=(25, 11))

    _plot_subplot("unique R", 'unq_R', 4, 1, activation_function, results)
    _plot_subplot("unique C", 'unq_C', 4, 2, activation_function, results)
    _plot_subplot("shared", 'shd', 4, 3, activation_function, results)
    _plot_subplot("synergistic", 'syn', 4, 4, activation_function, results)
    plt.subplots_adjust(wspace=None, hspace=0.2)
    plt.savefig("pid_terms_" + activation_function + ".png")

    return


