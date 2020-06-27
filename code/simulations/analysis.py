
from idtxl import set_estimator


def calculate_metrics(R, C, outputs, calculate_pid):

    """

    :param R: Receptive input 'spike train'
    :param C: Contextual input 'spike train'
    :param outputs: A dictionary with keys the name of the activation function type and values the output array of that activation

    :return: results['<activation function>'][<'metric name'>]
    """

    failures = 0
    results = {}

    for acti_fun, X in outputs.items():

        # I(X:R|C)
        cmi_est = set_estimator.Estimator_cmi('jidt_discrete')
        mi_X_R_conC = cmi_est.estimate(var1=X, var2=R, conditional=C)

        #print("{0} I(X:R|C) = {1}".format(acti_fun, mi_X_R_conC))

        # I(X:C|R)
        cmi_est = set_estimator.Estimator_cmi('jidt_discrete')
        mi_X_C_conR = cmi_est.estimate(var1=X, var2=C, conditional=R)

        #print("{0} I(X:C|R) = {1}".format(acti_fun, mi_X_C_conR))

        # I(X:R:C) = I(X:R) - I(X:R|C)
        mi_est = set_estimator.Estimator_mi('jidt_discrete')
        mi_X_R = mi_est.estimate(var1=X, var2=R)
        mi_X_R_C = mi_X_R - mi_X_R_conC

        #print("{0} I(X:R:C) = {1}".format(acti_fun, mi_X_R_C))

        if calculate_pid:
            pid_est = set_estimator.Estimator_pid('pid_tartu')
            try:
                pid_estimates = pid_est.estimate(R, C, X, {})
            except:
                failures +=1
            #print("{0} I(X;R;C) = {1}".format(acti_fun, mi_X_R_C))
            pid_estimates = {'shd_s1_s2':0., 'syn_s1_s2':0., 'unq_s1':0., 'unq_s2':0.}

        results[acti_fun] = {'mi_X_R_conC':mi_X_R_conC,
                             'mi_X_C_conR':mi_X_C_conR,
                             'mi_X_R_C': mi_X_R_C,
                             'shd_R_C':pid_estimates['shd_s1_s2'],
                             'syn_R_C':pid_estimates['syn_s1_s2'],
                             'unq_R':pid_estimates['unq_s1'],
                             'unq_C':pid_estimates['unq_s2']}

    if failures > 0:
        print("Failures = {}".format(failures))

    return results

