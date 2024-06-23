#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 14:04:29 2023

@author: guiguiclaudon
"""

import igraph as ig
import matplotlib.pyplot as plt


def draw_tree(tree):
    """Draws the graph correspponding to the tree."""
    n = tree.length
    n_vertices = 1
    depth = tree.depth
    edges = []
    dico = {0: 0}
    level = 1

    while level <= depth:
        for i in range(2**level-1, 2**(level+1)-1):
            if tree.nodes[i].data_type != 'None':
                dico[i] = n_vertices
                n_vertices += 1
        level += 1

    for el in dico:
        if el != 0:
            edges.append((dico[el], dico[(el-1)//2]))

    graph = ig.Graph(n_vertices, edges)

    for el in dico.items():
        graph.vs[el[1]]['symbol'] = tree.nodes[el[0]].symbol

    graph.vs['root'] = [True if i == 0 else False for i in range(n)]
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.invert_yaxis()
    ig.plot(graph,
            target=ax,
            vertex_label=graph.vs[:n_vertices]["symbol"],
            layout='rt',
            vertex_color=['steelblue' if root else 'white'
                          for root in graph.vs['root']]
            )
    plt.show()


def draw_function(tree, param_list, Y_ref):
    """Draws the function corresponding to the tree,
    as well as the reference function."""
    n = len(param_list[0].values)
    X = param_list[0].values
    Y = tree.evaluate()
    if type(Y) is int:
        plt.plot(X, [Y]*n, 'b', label='estimation')
    else:
        plt.plot(X, Y, 'b', label='estimation')
    plt.plot(X, Y_ref, 'r--', label='reference')
    plt.xlabel(param_list[0].symbol)
    plt.ylabel('y')
    plt.title('comparative graph')
    plt.legend()
    plt.show()
