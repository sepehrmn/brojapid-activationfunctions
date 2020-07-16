import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def _plot_fig1_subplot(label, metric, number, results_zero_c, results_one_c):
    """Plot a subplot for figure 1.

    :param label: string - label of subplot
    :param metric: string - information theoretic metric
    :param number: int - number of the subplot
    :param results_zero_c: structured array - contains results of the analysis for when c == 0
    :param results_one_c: structured array - contains results of the analysis for when c == 1
    :return:
    """
    ax = plt.subplot(3, 1, number)

    X = np.unique(results_zero_c['r'])

    # Zero context - dashed
    Y = results_zero_c[np.where(np.logical_and(results_zero_c['activation_function'] == 'nocontext',
                                               results_zero_c['information_metric'] == metric))]['value']
    ax.plot(X, Y, color='k', ls='dashed', label="Zero Context")

    # Additive - squares
    Y = results_one_c[np.where(np.logical_and(results_one_c['activation_function'] == 'additive',
                                              results_one_c['information_metric'] == metric))]['value']
    ax.plot(X, Y, color='k', marker='s', ls=' ', label="Additive")

    # Modulatory - circles
    Y = results_one_c[np.where(np.logical_and(results_one_c['activation_function'] == 'modulatory',
                                              results_one_c['information_metric'] == metric))]['value']

    ax.plot(X, Y, color='k', marker='o', markerfacecolor='None', ls=' ', label="Modulatory")
    # Both - dotted
    Y = results_one_c[np.where(np.logical_and(results_one_c['activation_function'] == 'both',
                                              results_one_c['information_metric'] == metric))]['value']

    plt.yticks(np.arange(0, 0.6, step=0.1))

    if (number == 3):
        plt.yticks(np.arange(0, 0.3, step=0.05))
        ax.set_xlabel('Magnitude of R', fontsize=19)
    ax.set_ylabel('Information bits', fontsize=18)
    ax.xaxis.set_tick_params(labelsize=14)
    ax.yaxis.set_tick_params(labelsize=14)
    ax.plot(X, Y, color='k', ls='dotted', label="Both")
    ax.text(-0.045, -0.11, label, transform=ax.transAxes, fontsize=18, fontweight='bold')

    return

def plot_fig1(results):
    """Plot figure 1. Calls "_plot_fig1_subplot" for each subplot.

    :param results: structured array - contains results of the analysis
    :return: None
    """
    plt.figure(figsize=(13.2, 10.8))

    results_zero_c = results[np.where(np.isclose(results['c'], 0.0))]
    results_one_c = results[np.where(np.isclose(results['c'], 1.0))]

    # I(X;R;C)
    _plot_fig1_subplot('(a)', 'I_X_R_C', 1, results_zero_c, results_one_c)

    # I(X;R|C)
    _plot_fig1_subplot('(b)',  'I_X_R__C', 2, results_zero_c, results_one_c)

    # I(X;C|R)
    _plot_fig1_subplot('(c)',  'I_X_C__R', 3, results_zero_c, results_one_c)

    plt.subplots_adjust(wspace=None, hspace=0.2)
    plt.show()

    return


def _plot_fig2_subplot(label, metric, number, function, results):
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


def plot_fig2(results):
    """Plot figure 2. Calls "_plot_fig2_subplot"

    :param results: structured array - results of the analysis
    :return: None
    """
    plt.figure(figsize=(9, 10.8))

    _plot_fig2_subplot("(a)", 'I_X_C__R', 1, 'additive', results)
    _plot_fig2_subplot("(b)", 'I_X_C__R', 2, 'modulatory', results)
    _plot_fig2_subplot("(c)", 'I_X_C__R', 3, 'both', results)

    plt.subplots_adjust(wspace=None, hspace=0.2)
    plt.show()

    return

def plot_fig3(X, analytical_results, simulation_results):
    """Plot figure 3.

    :param X: array - the x axis of sample sizes
    :param analytical_results: structured array - analytical results
    :param simulation_results: structured array - simulation results
    :return: None
    """
    # For figure 3, only the case where r == 2 and c == 2 is relevant. So first only
    # those results are selected.
    Y_all = analytical_results[np.logical_and(np.isclose(analytical_results['c'], 2.0),
                                              np.isclose(analytical_results['r'], 2.0))]

    plt.figure(figsize=(19.2, 10.8))

    ax = plt.subplot(3, 1, 1)
    # For the first subplot, the I(X,R,C) for the modulatory activation function is needed.
    Y = Y_all[np.where(np.logical_and(Y_all['activation_function'] == 'modulatory',
                                  Y_all['information_metric'] == 'I_X_R_C'))]['value']
    Y = np.repeat(Y, X.shape[0])
    ax.set_ylabel('Information bits', fontsize=18)
    ax.set_ylim(0.0, 0.9)
    ax.plot(X, Y, color='k', ls='dotted')
    Y = simulation_results['I_X_R_C']
    ax.errorbar(X, Y, yerr=simulation_results['sd_I_X_R_C'], color='k', capsize=2)
    ax.xaxis.set_tick_params(labelsize=14)
    ax.yaxis.set_tick_params(labelsize=14)
    ax.text(-0.06, -0.11, '(a)', transform=ax.transAxes, fontsize=18, fontweight='bold')

    ax = plt.subplot(3, 1, 2)
    # For the second subplot, the I(X,R|C) for the modulatory activation function is needed.
    Y = Y_all[np.where(np.logical_and(Y_all['activation_function'] == 'modulatory',
                                                   Y_all['information_metric'] == 'I_X_R__C'))]['value']
    Y = np.repeat(Y, X.shape[0])
    ax.set_ylabel('Information bits', fontsize=18)
    ax.set_ylim(0.0, 0.5)
    ax.plot(X, Y, color='k', ls='dotted')
    Y = simulation_results['I_X_R__C']
    ax.errorbar(X, Y, yerr=simulation_results['sd_I_X_R__C'], color='k', capsize=2)
    ax.text(-0.06, -0.11, '(b)', transform=ax.transAxes, fontsize=18, fontweight='bold')
    ax.xaxis.set_tick_params(labelsize=14)
    ax.yaxis.set_tick_params(labelsize=14)

    ax = plt.subplot(3, 1, 3)
    # For the third subplot, the I(X,C|R) for the modulatory activation function is needed.
    Y = Y_all[np.where(np.logical_and(Y_all['activation_function'] == 'modulatory',
                                      Y_all['information_metric'] == 'I_X_C__R'))]['value']
    Y = np.repeat(Y, X.shape[0])
    ax.set_xlabel('Sample size', fontsize=19)
    ax.set_ylabel('Information bits', fontsize=18)
    ax.plot(X, Y, color='k', ls='dotted', label="I(X;C|R)")
    Y = simulation_results['I_X_C__R']
    ax.errorbar(X, Y, yerr=simulation_results['sd_I_X_C__R'], color='k', capsize=2)
    ax.text(-0.06, -0.11, '(c)', transform=ax.transAxes, fontsize=18, fontweight='bold')
    ax.xaxis.set_tick_params(labelsize=14)
    ax.yaxis.set_tick_params(labelsize=14)
    ax.set_ylim(-0.1, 0.3)

    plt.subplots_adjust(wspace=None, hspace=0.2)
    plt.show()

    return

