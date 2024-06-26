# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 13:52:31 2023

@author: guiguiclaudon
"""

import random as rd
import numpy as np


class Node:
    def __init__(self, data_type, symbol, values):
        self.symbol = symbol
        self.data_type = data_type
        self.values = values

    def __repr__(self):
        return self.symbol


class Tree:
    def __init__(self, name):
        self.name = name
        self.nodes = []
        self.depth = 0
        self.length = 0

    def __repr__(self):
        return str(self.nodes)

    def update_param(self):
        self.length = len(self.nodes)
        self.depth = int(np.log2(self.length+1)-1)
        return self.length, self.depth

    def get_children(self, cp):
        n = len(self.nodes)
        children = []

        if cp < n:
            children.append(cp)

            left_child = 2 * cp + 1
            right_child = 2 * cp + 2

            children += self.get_children(left_child
                                          ) + self.get_children(right_child)

        children.sort()
        return children

    def get_parent_num(cp):
        return (cp - 1) // 2

    def copy(self):
        tree = Tree(f'{self.name}_fuse')
        tree.nodes = self.nodes[:]
        tree.update_param()
        return tree

    def delete_line(tree):
        size_tree = tree.length
        depth_tree = tree.depth
        while all(tree.nodes[k].data_type == 'None'
                  for k in range(int(2**(depth_tree)-1),
                                 int(2**(depth_tree+1)-1))):
            for q in range(int(2**(depth_tree)), int(2**(depth_tree+1))):
                tree.nodes.pop(-1)
            size_tree, depth_tree = tree.update_param()

    def excess_el(self, other, cp):
        child = self.get_children(cp)
        depth_child = np.log2(len(child)+1) - 1
        diff_depth = other.depth - depth_child
        diff_el = 2**(self.depth+diff_depth+1) - 2**(self.depth+1)
        return int(diff_el)

    def get_depth(self, cp):
        if self.depth == 0:
            return 0

        for i in range(self.depth + 1):
            if cp >= 2**i - 1 and cp < 2**(i+1) - 1:
                return i

    def full(self, func_list, param_list, cst_list, depth):
        n_p = len(param_list)
        n_c = len(cst_list)
        n_f = len(func_list)
        for i in range(2**(depth+1)-1):
            if 2**depth-1 <= i <= 2**(depth+1):
                if rd.randint(0, 1) == 0:
                    self.nodes.append(param_list[rd.randint(0, n_p-1)])
                else:
                    self.nodes.append(cst_list[rd.randint(0, n_c-1)])
            else:
                self.nodes.append(func_list[rd.randint(0, n_f-1)])
        self.depth = depth
        self.length = len(self.nodes)

    def grow(self, func_list, param_list, cst_list, depth):
        n_p = len(param_list)
        n_c = len(cst_list)
        n_f = len(func_list)
        self.nodes = [func_list[rd.randint(0, n_f-1)]]
        none = Node('None', 'Ø', None)
        for i in range(1, 2**(depth+1)-1):
            if self.nodes[((i+1)//2)-1].data_type == 'function':
                if 2**depth-1 <= i <= 2**(depth+1):
                    if rd.randint(0, 1) == 0:
                        self.nodes.append(param_list[rd.randint(0, n_p-1)])
                    else:
                        self.nodes.append(cst_list[rd.randint(0, n_c-1)])
                else:
                    x = rd.randint(0, 2)
                    if x == 0:
                        self.nodes.append(param_list[rd.randint(0, n_p-1)])
                    elif x == 1:
                        self.nodes.append(cst_list[rd.randint(0, n_c-1)])
                    else:
                        self.nodes.append(func_list[rd.randint(0, n_f-1)])
            else:
                self.nodes.append(none)
        self.delete_line()
        self.depth = depth
        self.length = len(self.nodes)

    def evaluate(self, index=0):
        size = self.length
        child1 = 2*index + 1
        child2 = 2*index + 2
        if child1 >= size:
            return self.nodes[index].values
        elif self.nodes[child1].data_type == 'None':
            return self.nodes[index].values
        elif self.nodes[index].values.data_type == 'operator':
            return self.nodes[index].values.operate(self.evaluate(child1),
                                                    self.evaluate(child2)
                                                    )
        else:
            return self.nodes[index].values.evaluate(self.evaluate(child1),
                                                     self.evaluate(child2)
                                                     )
