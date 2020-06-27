import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

def plot_fig1_subplot(title, metric, number, X, results_zero_c, results_one_c):

    ax = plt.subplot(3, 1, number)
    ax.set_title(title)
    ax.set_xlabel('r magnitude')
    ax.set_ylabel('Information bits')

    # Zero context - dashed
    Y = results_zero_c[np.where(np.logical_and(results_zero_c['activation_function'] == b'nocontext',
                                               results_zero_c['information_metric'] == metric))]['value']
    ax.plot(X, Y, color='k', ls='dashed', label="Zero Context")

    # Additive - squares
    Y = results_one_c[np.where(np.logical_and(results_one_c['activation_function'] == b'additive',
                                              results_one_c['information_metric'] == metric))]['value']
    ax.plot(X, Y, color='k', marker='s', ls=' ', label="Additive") # s is circle marker, markerfacecolor makes it hollow

    # Modulatory - circles
    Y = results_one_c[np.where(np.logical_and(results_one_c['activation_function'] == b'modulatory',
                                              results_one_c['information_metric'] == metric))]['value']
    # s is circle marker, markerfacecolor makes it hollow, ls linestyle makes it no line just marker
    ax.plot(X, Y, color='k', marker='o', markerfacecolor='None', ls=' ', label="Modulatory")
    # Both - dotted
    Y = results_one_c[np.where(np.logical_and(results_one_c['activation_function'] == b'both',
                                              results_one_c['information_metric'] == metric))]['value']
    ax.plot(X, Y, color='k', ls='dotted', label="Both")
    if number == 1:
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                   ncol=2, mode="expand", borderaxespad=0.)


def plot_fig1(X, results):

    fig = plt.figure()
    ax1 = plt.subplot(311)
    ax1.set_title('I(X;R;C)')
    ax1.set_xlabel('r magnitude')
    ax1.set_ylabel('Information bits')

    results_zero_c = results[np.where(np.isclose(results['c'], 0.0))]
    results_one_c = results[np.where(np.isclose(results['c'], 1.0))]

    # I(X;R;C)
    plot_fig1_subplot('I(X;R;C)', b'mi_X_R_C', 1, X, results_zero_c, results_one_c)

    # I(X;R|C)
    plot_fig1_subplot('I(X;R|C)',  b'mi_X_R_conC', 2, X, results_zero_c, results_one_c)

    # I(X;C|R)
    plot_fig1_subplot('I(X;C|R)',  b'mi_X_C_conR', 3, X, results_zero_c, results_one_c)

    plt.subplots_adjust(wspace=None, hspace=0.5)
    #plt.autoscale(tight=True)
    # plt.legend(bbox_to_anchor=(1.003, 3.), loc=2, borderaxespad=0.)
    plt.show()

def plot_fig2(X, Y, results):


    X, Y = np.meshgrid(X, Y)

    fig = plt.figure(figsize=(7, 15))
    fig.suptitle('I(X;C|R)', fontsize=14, fontweight='bold')

    # Subplot 1: Additive
    ax1 = plt.subplot(3, 1, 1, projection='3d')
    ax1.set_title('Additive')
    ax1.set_xlabel('R magnitude')
    ax1.set_ylabel('C magnitudes')
    ax1.set_zlabel('Information bits')
    Z = results[np.where(np.logical_and(results['activation_function'] == b'additive', results['information_metric']
                                         == b'mi_X_C_conR'))]['value']
    Z = Z.reshape(11, 11).T
    ax1.plot_wireframe(X, Y, Z)

    #
    ax2 = plt.subplot(3, 1, 2, projection='3d')
    ax2.set_title('Modulatory')
    ax2.set_xlabel('R magnitude')
    ax2.set_ylabel('C magnitudes')
    Z = results[np.where(np.logical_and(results['activation_function'] == b'modulatory', results['information_metric']
                                         == b'mi_X_C_conR'))]['value']
    Z = Z.reshape(11, 11).T
    ax2.set_zlabel('Information bits')
    ax2.plot_wireframe(X, Y, Z)

    ax3 = plt.subplot(3, 1, 3, projection='3d')
    ax3.set_title('Both')
    ax3.set_xlabel('R magnitude')
    ax3.set_ylabel('C magnitudes')
    Z = results[np.where(np.logical_and(results['activation_function'] == b'both', results['information_metric']
                                         == b'mi_X_C_conR'))]['value']
    Z = Z.reshape(11, 11).T
    ax3.set_zlabel('Information bits')
    ax3.plot_wireframe(X, Y, Z)

    plt.subplots_adjust(wspace=None, hspace=0.5)
    plt.show()

    return


# Plotting PID
def plot_pids_subplot(title, function, metric, number, X, Y, results):

    rnum = 1 if number % 2 == 1 else 2
    cnum = 1 if number <= 2 else 2
    ax = plt.subplot(2, 2, number, projection='3d')

    Z = results[np.where(np.logical_and(results['activation_function'] == function, results['information_metric']
                                        == metric))]['value']
    Z = Z.reshape(11, 11).T

    ax.set_title(title)
    ax.set_xlabel('R magnitude')
    ax.set_ylabel('C magnitudes')
    ax.set_zlabel('Information bits')
    ax.plot_wireframe(X, Y, Z)

    return

def plot_function_pid(title, function, X, Y, results):

    fig = plt.figure(figsize=(10, 15))
    fig.suptitle(title, fontsize=14, fontweight='bold')

    # 'shd_R_C' SI(X:R;C)
    plot_pids_subplot('SI(X:R;C)', function, b'shd_R_C', 1, X, Y, results)

    # 'syn_R_C' CI(X:R;C)
    plot_pids_subplot('CI(X:R;C)', function, b'syn_R_C', 2, X, Y, results)

    # 'unq_R' UI(X:C\R)
    plot_pids_subplot('UI(X:C\R)', function, b'unq_R', 3, X, Y, results)

    # 'unq_C' UI(X:R\C)
    plot_pids_subplot('UI(X:R\C)', function, b'unq_C', 4, X, Y, results)

    plt.subplots_adjust(wspace=None, hspace=0.5)
    plt.show()

    return

def plot_pids(X, Y, results):

    X, Y = np.meshgrid(X, Y)

    # additive
    plot_function_pid("Additive", b'additive', X, Y, results)

    # modulatory
    plot_function_pid("Modulatory", b'modulatory', X, Y, results)

    # both
    plot_function_pid("Both", b'both', X, Y, results)

    # nocontext
    plot_function_pid("no context", b'nocontext', X, Y, results)

    return

def plot_spectra(X, Y, results):

    return


