# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 18:28:01 2023

@author: aitsl
"""

import random as rd
import evolve as evolve
import numpy as np
import objects as ob
import graphing as gr
import matplotlib.pyplot as plt
import data as d


def generate_population(family_size, mode):
    init_pop = [ob.Tree(i) for i in range(family_size)]
    if mode == 1:
        for tree in init_pop:
            tree.full(d.func_list, d.param_list, d.cst_list, d.depth_init)
    else:
        for tree in init_pop:
            tree.grow(d.func_list, d.param_list, d.cst_list, d.depth_init)
    return init_pop


def fitness(tree):
    return sum(np.abs(d.Y_ref-tree.evaluate()))


def tournament(list_tree):
    k = rd.randint(1, len(list_tree))
    weight_pop = weight(list_tree)
    chosen_keep = rd.sample([tree for tree in list_tree],
                             k,
                             counts=[weight_pop[i][0] for i in range(len(weight_pop))]
                             )
    return min_fit(chosen_keep)


def weight(list_tree):
    size = len(list_tree)
    fit_pop = [fitness(list_tree[i]) for i in range(size)]
    total_fit = sum(fit_pop)
    weight_pop = [(int(100*(total_fit-fitness(list_tree[i]))/((size-1)*total_fit)),
                   list_tree[i]) for i in range(size)
                  ]
    return weight_pop


def min_fit(pop):
    fit_pop = [(fitness(pop[i]), i, pop[i]) for i in range(len(pop))]
    minfit = min(fit_pop)
    return minfit


def genetic():
    pop = generate_population(d.family_size//2, 1) + generate_population(d.family_size - d.family_size//2 , 0)
    minfit = min_fit(pop)
    best_tree = minfit[2]
    best_tree2 = best_tree
    it = 0
    fit = [minfit[0]]
    while fitness(best_tree2) > d.accuracy:
        it += 1
        print(f'iteration = {it}')
        new_gen = []
        if it >= d.max_it:
            print(f'max iteration reached: {it}, fitness = {fit[-1]})')
            return (best_tree2, fit)
        for tree in pop:
            tree.delete_line()
        weight_tree = weight(pop)
        num_mutate = int(d.family_size*d.mutate_rate)
        chosen_mutate = rd.sample([tree for tree in pop], num_mutate, counts=[weight_tree[i][0] for i in range (d.family_size)])
        for chosen in chosen_mutate:
            new_gen.append(evolve.mutate(d.func_list, d.param_list, d.cst_list, chosen))
        num_fuse = int(d.family_size*d.fuse_rate)
        for i in range(num_fuse):
            parent1 = tournament(pop)[2]
            parent2 = tournament(pop)[2]
            new_gen.append(evolve.fuse(parent1, parent2))
        num_keep = d.family_size - num_fuse - num_mutate
        chosen_keep = rd.sample([tree for tree in pop], num_keep, counts=[weight_tree[i][0] for i in range (d.family_size)])
        for chosen in chosen_keep:
            new_gen.append(chosen)
        pop = new_gen[:]
        minfit = min_fit(pop)
        best_tree = minfit[2]
        if fitness(best_tree) < fitness(best_tree2):
            best_tree2 = best_tree
        fit.append(fitness(best_tree2))
        if it % (d.max_it//d.affichage) == 0:
            gr.draw_tree(best_tree2)
            gr.draw_function(best_tree2, d.param_list, d.Y_ref)

    return (best_tree2, fit)


if __name__ == "__main__":
    data1, data2 = genetic()
    gr.draw_tree(data1)
    gr.draw_function(data1, d.param_list, d.Y_ref)
    X2 = [i for i in range(len(data2))]
    plt.plot(X2, data2)
    plt.show()
