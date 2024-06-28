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
             ob.Node('function', '@', op.divOperator),
             ob.Node('function', 'sin', op.fonction_sin)
             ]


X = ob.Node('parameter', 'x', np.linspace(-np.pi/2, np.pi/2, 500))
param_list = [X]
Y_ref = np.sin(X.values)**2 + np.sin(X.values) + 1
cst_list = constants(-5, 5, 10)


def repack_tree(printed_tree):
    printed_tree = printed_tree[1:-1].split(', ')
    return printed_tree


def symbols_to_tree(list_symbols, name_tree='tree'):
    tree = ob.Tree(name_tree)
    for symbol in list_symbols:
        added = False
        for i, func in enumerate(func_list):
            if symbol == func.symbol:
                tree.nodes.append(func_list[i])
                added = True
                continue
        for i, param in enumerate(param_list):
            if symbol == param.symbol:
                tree.nodes.append(param_list[i])
                added = True
                continue
        if not added and symbol != 'Ø':
            tree.nodes.append(ob.Node('constant', symbol, int(symbol)))
        if not added and symbol == 'Ø':
            tree.nodes.append(ob.Node('None', 'Ø', None))
    tree.update_param()
    return tree


testTree2 = symbols_to_tree(['@',
                             '@', '-',
                             'x', '*', '+', '@',
                             'Ø', 'Ø', '1', '-', '-2', '-', 'x', 'x',
                             'Ø', 'Ø', 'Ø', 'Ø', 'Ø', 'Ø', '5', '5',
                             'Ø', 'Ø', '1', '-2', 'Ø', 'Ø', 'Ø', 'Ø'],
                            'testTree2'
                            )

testTree3 = symbols_to_tree(['@',
                             '+', 'sin',
                             '-', '-', '-1', '@',
                             'x', '-1', 'x', 'x', 'Ø', 'Ø', 'x', 'x'],
                            'testTree3'
                            )

printed_tree4 = '[*, *, 1, x, *, Ø, Ø, Ø, Ø, +, 1, Ø, Ø, Ø, Ø, Ø, Ø, Ø, Ø, x, 1, Ø, Ø, Ø, Ø, Ø, Ø, Ø, Ø, Ø, Ø]'
tree_symbs4 = repack_tree(printed_tree4)
testTree4 = symbols_to_tree(tree_symbs4, 'testTree4')

family_size = 15

accuracy = 10**(-4)
depth_init = 2
max_depth = 3
max_it = 100

mutate_rate = 0.5
fuse_rate = 0.25

drawing_display_rate = 2
iteration_display_rate = 1
