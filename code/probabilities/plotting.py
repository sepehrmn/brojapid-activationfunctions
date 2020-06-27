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

    results_zero_c = results[np.where(np.isclose(results['c'], 0.0))]
    results_one_c = results[np.where(np.isclose(results['c'], 1.0))]

    # I(X;R;C)
    plot_fig1_subplot('I(X;R;C)', b'I_X_R_C', 1, X, results_zero_c, results_one_c)

    # I(X;R|C)
    plot_fig1_subplot('I(X;R|C)',  b'I_X_R__C', 2, X, results_zero_c, results_one_c)

    # I(X;C|R)
    plot_fig1_subplot('I(X;C|R)',  b'I_X_C__R', 3, X, results_zero_c, results_one_c)

    plt.subplots_adjust(wspace=None, hspace=0.5)
    #plt.autoscale(tight=True)
    # plt.legend(bbox_to_anchor=(1.003, 3.), loc=2, borderaxespad=0.)
    plt.show()

# FIG 2
def _plot_MI_subplot(metric, number, function, X, Y, results):

    X, Y = np.meshgrid(X, Y)
    n_points = X.shape[0]

    # Subplot 1: Additive
    ax = plt.subplot(3, 1, number, projection='3d')
    ax.set_title(function.decode('utf-8'))
    ax.set_xlabel('|r|')
    ax.set_ylabel('|c|')
    ax.set_zlabel('Information bits')
    Z = results[np.where(np.logical_and(results['activation_function'] == function, results['information_metric']
                                         == metric))]['value']
    Z = Z.reshape(n_points, n_points).T
    ax.plot_surface(X, Y, Z, color="orange")


def _plot_MI(title, metric, X, Y, results):

    fig = plt.figure() # figsize=(7, 15))
    fig.suptitle(title, fontsize=14, fontweight='bold')

    # title, metric, number, X, Y, results, color
    _plot_MI_subplot(metric, 1, b'additive', X, Y, results)

    # title, metric, number, X, Y, results, color
    _plot_MI_subplot(metric, 2, b'modulatory', X, Y, results)

    # title, metric, number, X, Y, results, color
    _plot_MI_subplot(metric, 3, b'both', X, Y, results)

    plt.subplots_adjust(wspace=None, hspace=0.5)
    plt.show()

    return

def plot_MIs(X, Y, results):

    # Subplot 1: Additive
    _plot_MI('I(X;R|C)', b'I_X_R__C', X, Y, results)

    _plot_MI('I(X;C|R)', b'I_X_C__R', X, Y, results)

    _plot_MI('I(X;C;R)', b'I_X_R_C', X, Y, results)

    return

# FIG 3
# Plotting PID
def plot_pids_subplot(title, function, metric, number, X, Y, results, color):

    n_points = X.shape[0]
    ax = plt.subplot(2, 2, number, projection='3d')

    Z = results[np.where(np.logical_and(results['activation_function'] == function, results['information_metric']
                                        == metric))]['value']
    Z = Z.reshape(n_points, n_points).T

    ax.set_title(title)
    ax.set_xlabel('a (|r|)', fontsize=12, fontweight='bold')
    ax.set_ylabel('b (|c|)', fontsize=12, fontweight='bold')
    ax.set_zlabel('Information bits')
    ax.plot_surface(X, Y, Z, color=color)

    return

def plot_function_pid(title, function, X, Y, results):

    # fig = plt.figure(figsize=(10, 15))
    fig = plt.figure()
    fig.suptitle(title, fontsize=14, fontweight='bold')

    # 'shd_R_C' SI(X:R;C)
    plot_pids_subplot('Shared', function, b'shd_R_C', 1, X, Y, results, "green")

    # 'syn_R_C' CI(X:R;C)
    plot_pids_subplot('Synergistic', function, b'syn_R_C', 2, X, Y, results, "Orange")

    # 'unq_R' UI(X:C\R)
    plot_pids_subplot('Unqiue X1', function, b'unq_R', 3, X, Y, results, "Blue")

    # 'unq_C' UI(X:R\C)
    plot_pids_subplot('Unique X2', function, b'unq_C', 4, X, Y, results, "Yellow")

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

    # nocontext -
    # plot_function_pid("no context", b'nocontext', X, Y, results) #TODO: Check what happens. Why can it still plot this?

    return

def _plot_spectra_subplot(a, b, corr, results, function):

    # metrics = [UX1, UX2, Shd, Syn, Hy, I12, Hx1, Hx2]

    #
    # UX1 = blue
    # UX2 = yellow
    # Shd = green
    # Syn = orange
    # Hy = red
    # I12_r = purple
    # Hx1 = pink
    # Hx2 = lightblue

    width = 35
    #metrics = [UX1, UX2, Shd, Syn, Hy, I12, Hx1, Hx2]

    plt.bar(width, 4, color=['blue', 'yellow', 'green', 'orange']) #, 'red', 'purple', 'pink', 'lightblue']) #

    'additive'
    'modulatory'

    f = plt.figure()
    ax1 = f.add_subplot(1, 1, 1)

    ax1.setylabel()
    ax1.setx_labels([])

    return

def plot_spectra(a, b, corr, results):
    '''
        normalized spectra
    :param a: 
    :param b: 
    :param results: 
    :return: 
    '''

    _plot_spectra_subplot(a, b, corr, results, b'additive')

    _plot_spectra_subplot(a, b, corr, results, b'modulatory')

    _plot_spectra_subplot(a, b, corr, results, b'both')

    return

def plot_wibral_pids(X, Y, results):
    # import matplotlib
    # matplotlib.use('Agg')
    # matplotlib.rcParams['axes.labelpad'] = 10.
    def plot_wibral_pid_subplot(title, function, metric, number, X, Y, results, color):
        X, Y = np.meshgrid(X, Y)

        n_points = X.shape[0]
        ax = plt.subplot(2, 4, number, projection='3d')

        Z = results[np.where(np.logical_and(results['activation_function'] == function, results['information_metric']
                                            == metric))]['value']
        Z = Z.reshape(n_points, n_points).T

        if number < 5:
            ax.set_title(title, fontsize=19, fontweight='bold', y=1.17)
        ax.set_xlabel('X1', fontsize=16, fontweight='bold', labelpad=5.)
        ax.set_ylabel('X2', fontsize=16, fontweight='bold', labelpad=5.)
        ax.set_zlabel('Information bits', fontsize=14, fontweight='bold', labelpad=13.)
        if number == 8:
            ax.set_zlim(zmin=0.)
        ax.plot_surface(X, Y, Z, color=color)

    fig = plt.figure()
    #fig.suptitle("Partial Information Decomposition", fontsize=14, fontweight='bold')

    indices = [1, 2, 3, 4, 5, 6, 7, 8]

    plot_wibral_pid_subplot('Shared', b'additive', b'shd_R_C', indices[0], X, Y, results, "blue")
    # 'syn_R_C' CI(X:R;C)
    plot_wibral_pid_subplot('Synergistic', b'additive', b'syn_R_C', indices[1], X, Y, results, "Red")
    # 'unq_R' UI(X:C\R)
    plot_wibral_pid_subplot('Unqiue X1', b'additive', b'unq_R', indices[2], X, Y, results, "darkolivegreen")
    # 'unq_C' UI(X:R\C)
    plot_wibral_pid_subplot('Unique X2', b'additive', b'unq_C', indices[3], X, Y, results, "lime")
    #************************************************************************************************
    #******************* Modulatory
    plot_wibral_pid_subplot('Shared', b'modulatory', b'shd_R_C', indices[4], X, Y, results, "blue")
    # 'syn_R_C' CI(X:R;C)
    plot_wibral_pid_subplot('Synergistic', b'modulatory', b'syn_R_C', indices[5], X, Y, results, "Red")
    # 'unq_R' UI(X:C\R)
    plot_wibral_pid_subplot('Unqiue X1', b'modulatory', b'unq_R', indices[6], X, Y, results, "darkolivegreen")
    # 'unq_C' UI(X:R\C)
    plot_wibral_pid_subplot('Unique X2', b'modulatory', b'unq_C', indices[7], X, Y, results, "lime")

    plt.subplots_adjust(wspace=0.26, hspace=0.05)
    plt.show()


    return