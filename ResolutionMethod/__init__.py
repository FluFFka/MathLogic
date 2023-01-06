from Formulas import *
from random import randrange, shuffle

class Disjunct:
    def __init__(self, *predicates):    # could be Formula('~', Predicate)
        self.predicates = list(predicates)
    def __str__(self):
        str_preds = []
        for predicate in self.predicates:
            str_preds.append(str(predicate))
        return ' V '.join(str_preds)


class Disjunct_set:
    def __init__(self, *disjuncts):
        self.disjuncts = list(disjuncts)
    def __str__(self):
        str_disjs = []
        for disjunct in self.disjuncts:
            str_disjs.append(str(disjunct))
        return ', '.join(str_disjs)


def extract_disjunct_set(formula):
    if isinstance(formula, Predicate) or formula.operation == '~':
        return Disjunct_set(Disjunct(formula))
    elif formula.operation == '&':
        ds1 = extract_disjunct_set(formula.formulas[0])
        ds2 = extract_disjunct_set(formula.formulas[1])
        ds1.disjuncts += ds2.disjuncts
        return ds1
    elif formula.operation == 'V':
        ds1 = extract_disjunct_set(formula.formulas[0])
        ds2 = extract_disjunct_set(formula.formulas[1])
        if len(ds1.disjuncts) != 1 or len(ds2.disjuncts) != 1:
            print('Wrong disjuncts')
            exit(1)
        ds1.disjuncts[0].predicates += ds2.disjuncts[0].predicates
        return ds1
    else:
        return extract_disjunct_set(formula.formulas[0])    # 'A' or 'E'


def unify_predicates(predicate1, predicate2):   # also unify Formula('~', Predicate)
    if isinstance(predicate1, Formula):
        predicate1 = predicate1.formulas[0]
        predicate2 = predicate2.formulas[0]
    eq_system = []
    for i in range(len(predicate1.args)):
        eq_system.append([predicate1.args[i], predicate2.args[i]])
    
    unified = False
    while not unified:
        eq_system2 = []
        for i in range(len(eq_system)):
            for j in range(i + 1, len(eq_system)):
                if eq_system[i] == eq_system[j]:
                    break
            else:
                eq_system2.append(eq_system[i])
        eq_system = eq_system2
        eq_ind = randrange(len(eq_system))
        eq_ind_start = eq_ind
        changed = False
        while (not changed):
            curr_eq = eq_system[eq_ind]
            if curr_eq[0] == curr_eq[1]:
                eq_system = eq_system[:eq_ind] + eq_system[eq_ind + 1:]
                changed = True
            elif (not isinstance(curr_eq[0], Variable)) and isinstance(curr_eq[1], Variable):
                eq_system[eq_ind] = curr_eq[::-1]
                changed = True
            elif isinstance(curr_eq[0], Functional) and isinstance(curr_eq[1], Functional):
                if curr_eq[0].name != curr_eq[1].name:
                    return None
                eq_system = eq_system[:eq_ind] + eq_system[eq_ind + 1:]
                for i in range(len(curr_eq[0].args)):
                    eq_system.append([curr_eq[0].args[i], curr_eq[1].args[i]])
                changed = True
            elif isinstance(curr_eq[0], Variable) and not curr_eq[1].contains(curr_eq[0]):
                for i in range(len(eq_system)):
                    if i == eq_ind:
                        continue
                    if curr_eq[0] == eq_system[i][0] and curr_eq[0] != eq_system[i][1]:
                        return None
                    if isinstance(eq_system[i][1], Variable) and eq_system[i][1] == curr_eq[0]:
                        eq_system[i][1] = curr_eq[1]
                        changed = True
                    if isinstance(eq_system[i][1], Functional) and eq_system[i][1].contains(curr_eq[0]):
                        eq_system[i][1].put_term(curr_eq[0].name, curr_eq[1])
                        changed = True
            eq_ind = (eq_ind + 1) % len(eq_system)
            if eq_ind == eq_ind_start:
                unified = True
                break
    return eq_system


def resolution_method(formula: Formula, output=False):
    formula = Formula('~', formula.copy())
    if output:
        print('Negated:', str(formula))
        print('PNF conversion')
    formula.rename_variables(dict(), dict())
    if output:
        print('Rename variables:', str(formula))
    formula.remove_implications()
    if output:
        print('Remove implications:', str(formula))
    formula = Formula('#', formula) # filler operation to remove possible double negations in front
    formula.move_negations()
    formula = formula.formulas[0]
    if output:
        print('Move negations:', str(formula))
    formula.move_quantifiers()
    if output:
        print('Move quantifiers:', str(formula))
    formula.transform_to_CNF()
    if output:
        print('Transform to CNF:', str(formula))
    formula.transform_to_SNF(dict(), [])
    if output:
        print('Transform to SNF:', str(formula))
    disjunction_set = extract_disjunct_set(formula)
    if output:
        print('Disjunction set:', str(disjunction_set))
    return True