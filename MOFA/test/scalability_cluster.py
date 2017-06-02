import numpy as np
import os

res_dir = '/homes/arnol/test/'


K_vals = np.linspace(5.0, 99.0, num=20, dtype=int)
D_vals = np.linspace(500.0, 10000.0, num=20, dtype=int)
N_vals = np.linspace(100.0, 2000.0, num=20, dtype=int)
M_vals = np.linspace(2.0, 20.0, num=20, dtype=int)


# test K
it_ix = 0
for val in K_vals:
    for i in range(3):
        command = 'bsub  -o tmp_log -M 8000 python multiple_tests.py' + ' ' + \
                    'K' + ' ' + \
                    res_dir + ' ' + \
                    str(val) + ' ' + \
                    str(it_ix)
        os.system(command)
        it_ix+=1

# test D
it_ix = 0
for val in D_vals:
    for i in range(3):
        command = 'bsub  -o tmp_log -M 8000 python multiple_tests.py' + ' ' + \
                    'D' + ' ' + \
                    res_dir + ' ' + \
                    str(val) + ' ' + \
                    str(it_ix)
        os.system(command)
        it_ix+=1

# test N
it_ix = 0
for val in N_vals:
    for i in range(3):
        command = 'bsub  -o tmp_log -M 8000 python multiple_tests.py' + ' ' + \
                    'N' + ' ' + \
                    res_dir + ' ' + \
                    str(val) + ' ' + \
                    str(it_ix)
        os.system(command)
        it_ix+=1

# test M
it_ix = 0
for val in M_vals:
    for i in range(3):
        command = 'bsub  -o tmp_log -M 8000 python multiple_tests.py' + ' ' + \
                    'M' + ' ' + \
                    res_dir + ' ' + \
                    str(val) + ' ' + \
                    str(it_ix)
        os.system(command)
        it_ix+=1