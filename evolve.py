# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 19:43:39 2023

@author: nolan
"""

import random as rd
import objects as ob
import data as d


def fuse(tree_ini, tree_add):
    tree = tree_ini.copy()
    t_add = tree_add.copy()

    n = tree.length
    if tree.depth < d.max_depth:
        cp = rd.randint(0, n-1)  # crossover point
        while tree.nodes[cp].data_type == 'None':
            cp = rd.randint(0, n-1)

    else:
        firs_el_last_level_tree = 2**d.max_depth - 1
        max_cp = firs_el_last_level_tree - 1
        cp = rd.randint(0, max_cp)  # crossover point
        while tree.nodes[cp].data_type == 'None':
            cp = rd.randint(0, max_cp)

    cp_depth = tree.get_depth(cp)
    max_depth_t_add = d.max_depth - cp_depth
    min_cp_add = 2**(t_add.depth - max_depth_t_add) - 1
    if min_cp_add < 0:
        min_cp_add = 0

    firs_el_last_level_t_add = 2**t_add.depth - 1
    max_cp_add = firs_el_last_level_t_add - 1
    cp_add = rd.randint(min_cp_add, max_cp_add)
    while t_add.nodes[cp_add].data_type == 'None' or t_add.nodes[cp_add].data_type == 'constant' or t_add.nodes[cp_add].data_type == 'parameter':
        cp_add = rd.randint(min_cp_add, max_cp_add)

    children_add = t_add.get_children(cp_add)
    t_add.nodes = []
    for i in range(len(children_add)):
        t_add.nodes.append(tree_add.nodes[children_add[i]])
    t_add.update_param()

    children = tree.get_children(cp)
    n_ch = len(children)
    n_ta = t_add.length
    if n_ch > n_ta:
        for i in range(n_ta):
            tree.nodes[children[i]] = t_add.nodes[i]
        for j in range(n_ta, n_ch):
            tree.nodes[children[j]] = ob.Node('None', 'Ø', None)

    elif n_ch < n_ta:
        diff_el = tree.excess_el(t_add, cp)
        for i in range(diff_el):
            tree.nodes.append(ob.Node('None', 'Ø', None))
        children_2 = tree.get_children(cp)
        for j in range(n_ta):
            tree.nodes[children_2[j]] = t_add.nodes[j]

    else:
        for i in range(n_ch):
            tree.nodes[children[i]] = t_add.nodes[i]

    tree.delete_line()
    tree.update_param()
    return tree


def mutate(func_list, param_list, cst_list, tree_ini):
    tree = ob.Tree(f'{tree_ini.name}_mutate')
    tree.nodes = tree_ini.nodes[:]
    tree.update_param()
    sub_tree = ob.Tree(f'{tree_ini.name}_1')
    sub_tree.grow(func_list, param_list, cst_list, rd.randint(2, 4))
    sub_tree.delete_line()
    sub_tree.update_param()

    return fuse(tree, sub_tree)
