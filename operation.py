# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Fra Jan 19 14:28:20 2024

@author: nolan
"""

import numpy as np


class intervalle_coupe:
    def __init__(self,
                 intervalle1,
                 intervalle2,
                 inf2,
                 sup2
                 ):
        self.intervalle1 = intervalle1
        self.intervalle2 = intervalle2
        self.inf2 = inf2
        self.sup2 = sup2

    def is_in(self, x):
        if f'{type(x)}' == "<class 'numpy.ndarray'>":
            size = len(x)
            inf1 = np.array([min(self.intervalle1.inf,
                                 self.intervalle2.inf
                                 )]*size)
            sup1 = np.array([self.inf2]*size)
            inf2 = np.array([self.sup2]*size)
            sup2 = np.array([max(self.intervalle1.sup,
                                 self.intervalle2.sup
                                 )]*size)
            return ((inf1 < x).any() and (x < sup1).any()
                    ) or ((inf2 < x).any() and (x < sup2).any()
                          )
        else:
            return (min(self.intervalle1.inf,
                        self.intervalle2.inf
                        ) < x < self.inf2
                    ) or (self.sup2 < x < max(self.intervalle1.sup,
                                              self.intervalle2.sup
                                              )
                          )

    def __repr__(self):
        lower_bound1 = str(min(self.intervalle1.inf, self.intervalle2.inf))
        upper_bound1 = str(self.inf2)
        lower_bound2 = str(self.sup2)
        upper_bound2 = str(max(self.intervalle1.sup, self.intervalle2.sup))
        return f']{lower_bound1}:{upper_bound1}[U{lower_bound2}:{upper_bound2}['


class intervalle_ouvert:
    def __init__(self, inf, sup):
        self.inf = inf
        self.sup = sup

    def is_in(self, x):
        if f'{type(x)}' == "<class 'numpy.ndarray'>":
            size = len(x)
            inf1 = np.array([self.inf]*size)
            sup1 = np.array([self.sup]*size)
            return (inf1 < x).any() and (x < sup1).any()
        else:
            return self.inf < x < self.sup

    def __repr__(self):
        return "]" + str(self.inf) + ":" + str(self.sup) + "["

    def union(self, other):
        n = min(self.inf, other.inf)
        N = max(self.inf, other.inf)
        m = min(self.sup, other.sup)
        M = max(self.sup, other.sup)
        if m <= N:
            return intervalle_coupe(self, other, m, N)
        else:
            return intervalle_ouvert(n, M)


R = intervalle_ouvert(float("-inf"), float("inf"))
R_plus = intervalle_ouvert(0, float("inf"))
R_moins = intervalle_ouvert(float("-inf"), 0)
R_etoile = R_plus.union(R_moins)


class Function_prot:
    def __init__(self, ensemble_definition, expression):
        self.E = ensemble_definition
        self.f = expression
        self.data_type = 'function_prot'

    def evaluate(self, x, y):
        if self.E.is_in(x+y):
            return self.f(x+y)
        else:
            return 1


def fonction_inverse(x):
    return 1/x


fonction_inverse_protege = Function_prot(R_etoile, fonction_inverse)
fonction_exponentielle = Function_prot(R, np.exp)
fonction_log_protege = Function_prot(R_plus, np.log)
fonction_sin = Function_prot(R, np.sin)
fonction_cos = Function_prot(R, np.cos)


class Operator:
    def __init__(self, f):
        self.f = f
        self.data_type = 'operator'

    def operate(self, a, b):
        return self.f(a, b)


def addition(a, b):
    return a+b


def soustraction(a, b):
    return a - b


def multiplication(a, b):
    return a*b


def division(a, b):
    return a*fonction_inverse_protege.evaluate(b, 0)


addOperator = Operator(addition)
subsOperator = Operator(soustraction)
multOperator = Operator(multiplication)
divOperator = Operator(division)
