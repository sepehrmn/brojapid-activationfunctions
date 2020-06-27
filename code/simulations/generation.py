import random
import numpy as np


def gen_input(n_samples, r_firing, r_silent, c_firing, c_silent):

    R = np.zeros(n_samples, dtype=np.float)
    C = np.zeros(n_samples, dtype=np.float)
    P_C_givR = 0.889972
    P_R_C = 0.5 * P_C_givR
    P_R_notC = 0.5 * (1 - P_C_givR)
    P_notR_C = 0.5 * (1 - P_C_givR)
    P_notR_notC = 0.5 * P_C_givR

    for sampnum in range(n_samples):

        rn = random.random()

        if rn < P_R_C:
            R[sampnum] = r_firing
            C[sampnum] = c_firing

        elif rn < (P_R_C + P_R_notC):
            R[sampnum] = r_firing
            C[sampnum] = c_silent

        elif rn < (P_R_C + P_R_notC + P_notR_C):
            R[sampnum] = r_silent
            C[sampnum] = c_firing

        else:
            R[sampnum] = r_silent
            C[sampnum] = c_silent

    return R, C

# def gen_input(n_samples, r_firing, r_silent, c_firing, c_silent):
#
#     R = np.zeros(n_samples, dtype=np.int)
#     C = np.zeros(n_samples, dtype=np.int)
#
#     for sampnum in range(n_samples):
#
#         rn = random.random()
#
#         if rn < 0.25:
#             R[sampnum] = r_firing
#             C[sampnum] = c_firing
#
#         elif rn < 0.5:
#             R[sampnum] = r_firing
#             C[sampnum] = c_silent
#
#         elif rn < 0.75:
#             R[sampnum] = r_silent
#             C[sampnum] = c_firing
#
#         else:
#             R[sampnum] = r_silent
#             C[sampnum] = c_silent
#
#     return R, C


