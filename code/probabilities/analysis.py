import numpy as np
import math
import itertools

from idtxl import synergy_tartu
from idtxl import estimators_pid

def calculate_metrics(r, c, functions_x, functions_x__r, functions_x__c,
                      functions_x__r_c, functions_rcx, calculate_pid):

    functions = list(functions_rcx.keys())
    failures = 0
    results = {}

    for function in functions:

        x = functions_x[function]
        x__r = functions_x__r[function]
        x__c = functions_x__c[function]
        x__r_c = functions_x__r_c[function]
        rcx = functions_rcx[function]

        I_X_R__C = 0
        I_X_C__R = 0
        I_X_R_C = 0

        H_X = 0
        for letter_x in x:
            H_X += -x[letter_x] * math.log(x[letter_x] ,2)
        #
        # H_R =
        #
        # H_C =
        #
        # I_R_C =

        for letter_x, letter_r, letter_c in itertools.product(x, r, c):

            val_rcx = rcx[(letter_r, letter_c, letter_x)]
            val_x__r_c = x__r_c[(letter_x, letter_r, letter_c)]
            val_x__c = x__c[(letter_x, letter_c)]
            val_x__r = x__r[(letter_x, letter_r)]
            val_x = x[letter_x]

            # H(X)
            # H_X

            # H_X1X2|Y

            # H_Y|X1X2

            # I_X1_X2|Y

            # I(X;R|C)
            temp_I_X_R__C = 0.0
            try: # for ValueError: math domain error
                temp_I_X_R__C = val_rcx * math.log(val_x__r_c / val_x__c, 2)
            except:
                pass

            if not math.isnan(temp_I_X_R__C):
                I_X_R__C += temp_I_X_R__C


            # I(X;C|R)
            temp_I_X_C__R = 0.0  # slightly below
            try:
                temp_I_X_C__R = val_rcx * math.log(val_x__r_c / val_x__r, 2)
            except:
                pass

            if not math.isnan(temp_I_X_C__R):
                I_X_C__R += temp_I_X_C__R


            # I(X;R;C)
            temp_I_X_R_C = 0.0
            try:
                temp_I_X_R_C = val_rcx * math.log( (val_x__r * val_x__c) / (val_x * val_x__r_c), 2)
            except:
                pass

            if not math.isnan(temp_I_X_R_C):
                I_X_R_C += temp_I_X_R_C


        if calculate_pid:

            # Entropy of x

            # (t[i], s1[i], s2[i])  - providing PID in xrc form
            xrc = {}
            for letter_r, letter_c, letter_x in rcx:
                xrc[(letter_x,letter_r,letter_c)] = float(rcx[(letter_r, letter_c, letter_x)])

            g = synergy_tartu.pid(pdf_dirty=xrc)
            pid_estimates = {
                'syn_s1_s2': g['CI'],
                'shd_s1_s2': g['SI'],
                'unq_s1': g['UIY'],
                'unq_s2': g['UIZ'],
            }

        else:
            pid_estimates = {'shd_s1_s2':0., 'syn_s1_s2':0., 'unq_s1':0., 'unq_s2':0.}


        results[function] = {'H_X':H_X,
                             'I_X_R__C':I_X_R__C,
                             'I_X_C__R':I_X_C__R,
                             'I_X_R_C': I_X_R_C,
                             'shd_R_C':pid_estimates['shd_s1_s2']/H_X,
                             'syn_R_C':pid_estimates['syn_s1_s2']/H_X,
                             'unq_R':pid_estimates['unq_s1']/H_X,
                             'unq_C':pid_estimates['unq_s2']/H_X}

        if results[function]['unq_C'] < 0.00000001:
            results[function]['unq_C'] = 0.

        if results[function]['unq_R'] < 0.00000001:
            results[function]['unq_R'] = 0.

        if results[function]['syn_R_C'] < 0.00000001:
            results[function]['syn_R_C'] = 0.

        if results[function]['shd_R_C'] < 0.00000001:
            results[function]['shd_R_C'] = 0.

    #print("Number of PID failures = {}".format(failures))

    return results

