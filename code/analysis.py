import numpy as np
import math
import itertools
import idtxl.synergy_tartu as synergy_tartu

def cal_mis(R, C, X, X__R, X__C, X__R_C, RCX):
    """Calculates the three-way mutual and conditional mutual information terms based on probability distributions.

    :param R: dictionary - P(R)
    :param C: dictionary - P(C)
    :param X: dictionary - P(X)
    :param X__R: dictionary - P(X|R)
    :param X__C: dictionary - P(X|C)
    :param X__R_C: dictionary - P(X|R,C)
    :param RCX: dictionary - P(R,C,X)
    :return: returns a dictionary containing values for 'I_X_R__C', 'I_X_C__R', 'I_X_R_C'.
    """
    I_X_R__C = 0.0
    I_X_C__R = 0.0
    I_X_R_C = 0.0

    for x, r, c in itertools.product(X, R, C):

        val_rcx = RCX[(r, c, x)] + np.finfo(float).eps
        val_x__r_c = X__R_C[(x, r, c)] + np.finfo(float).eps
        val_x__c = X__C[(x, c)] + np.finfo(float).eps
        val_x__r = X__R[(x, r)] + np.finfo(float).eps
        val_x = X[x] + np.finfo(float).eps

        # I(X;R;C) - corresponds to equation 9 in the replication
        I_X_R_C += val_rcx * math.log((val_x__r * val_x__c) / (val_x * val_x__r_c), 2)

        # I(X;R|C) - corresponds to equation 10 in the replication
        I_X_R__C += val_rcx * math.log(val_x__r_c / val_x__c, 2)

        # I(X;C|R) - corresponds to equation 11 in the replication
        I_X_C__R += val_rcx * math.log(val_x__r_c / val_x__r, 2)

    
    # solver_args = {'keep_solver_object': False}
    # retval = synergy_tartu.pid(pdf_dirty=pdf,
    #                                cone_solver='ECOS',
    #                                output=int(False),
    #                                **{'keep_solver_object': False})

    retval = synergy_tartu.pid(pdf_dirty=RCX)
    
    results = {'I_X_R_C': I_X_R_C,
               'I_X_R__C': I_X_R__C,
               'I_X_C__R': I_X_C__R,
               'shd': retval['SI'],
               'syn': retval['CI'],
               'unq_R': retval['UIY'],
               'unq_C': retval['UIZ'],
               }
    

    return results


def cal_fun_met(R, C, functions_X, functions_X__R, functions_X__C,
                      functions_X__R_C, functions_RCX):
    """For each activation function, call 'cal_mis'.

    :param R: dictionary - P(R)
    :param C: dictionary - P(C)
    :param functions_X: dictionary - P(X) for each activation function
    :param functions_X__R: dictionary - P(X|R) for each activation function
    :param functions_X__C: dictionary - P(X|C) for each activation function
    :param functions_X__R_C: dictionary - P(X|R,C) for each activation function
    :param functions_RCX: dictionary - P(R,C,X) for each activation function
    :return: a dictionary containing 'I_X_R__C', 'I_X_C__R', 'I_X_R_C' for each activation function.
    """
    functions = list(functions_RCX.keys())
    results = {}

    for function in functions:

        X = functions_X[function]
        X__R = functions_X__R[function]
        X__C = functions_X__C[function]
        X__R_C = functions_X__R_C[function]
        RCX = functions_RCX[function]

        results[function] = cal_mis(R, C, X, X__R, X__C, X__R_C, RCX)

    return results
