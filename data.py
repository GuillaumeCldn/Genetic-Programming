# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 14:58:44 2024

@author: aitsl
"""

import objects as ob
import numpy as np
import random as rd
import operation as op


def constants(min_cst, max_cst, total_cst):
    L = []
    for _ in range(total_cst):
        a = rd.randint(min_cst, max_cst)
        L.append(ob.Node('constant', str(a), a))
    return L


func_list = [ob.Node('function', '+', op.addOperator),
             ob.Node('function', '-', op.subsOperator),
             ob.Node('function', '*', op.multOperator),
             # ob.Node('function', '@', op.divOperator),
             # ob.Node('function', 'sin', op.fonction_sin)
             ]


X = ob.Node('parameter', 'x', np.linspace(-np.pi/2, np.pi/2, 500))
param_list = [X]
Y_ref = (X.values)**3 - (X.values)**2 + (X.values) + 1
cst_list = constants(-5, 5, 10)

family_size = 15

accuracy = 10**(-4)
depth_init = 2
max_depth = 4
max_it = 500

mutate_rate = 0.5
fuse_rate = 0.25
drawing_display_rate = 4
iteration_display_rate = 25

plot_dir = "./plots/"
