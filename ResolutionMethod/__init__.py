from Formulas import *
from random import randrange

def collapse_disjunct(predicates, p1, p2):
    subst = unify_predicates(p1, p2)
    formula = p1
    for predicate in predicates:
        formula = Formula('V', predicate, formula)
    formula.put_terms(subst)
    formula.rename_full(dict())
    return extract_disjunct_set(formula).disjuncts[0]

def resolute_disjuncts(predicates1, predicates2, subst):    # predicates1 and predicates2 could be empty
    if len(predicates1) == 0 and len(predicates2) == 0:
        return [EmptyDisjunct()]
    if len(predicates1) != 0:
        formula = predicates1[0]
        for predicate in predicates1[1:]:
            formula = Formula('V', predicate, formula)
    else:
        formula = predicates2[0]
    for predicate in predicates2:
        formula = Formula('V', predicate, formula)
    formula.put_terms(subst)
    formula.rename_full(dict())
    return [extract_disjunct_set(formula).disjuncts[0]]

def resolution(disjunct1, disjunct2):
    formula1 = disjunct1.predicates[0]
    for predicate in disjunct1.predicates[1:]:
        formula1 = Formula('V', predicate, formula1)
    formula1.rename_full(dict())
    formula2 = disjunct2.predicates[0]
    for predicate in disjunct2.predicates[1:]:
        formula2 = Formula('V', predicate, formula2)
    formula2.rename_full(dict())
    d1, d2 = extract_disjunct_set(formula1).disjuncts[0], extract_disjunct_set(formula2).disjuncts[0]
    new_disjuncts = []
    for i in range(len(d1.predicates)):
        for j in range(len(d2.predicates)):
            if isinstance(d1.predicates[i], Formula) and d1.predicates[i].operation == '~' and isinstance(d2.predicates[j], Predicate):
                p1 = d1.predicates[i].formulas[0]
                p2 = d2.predicates[j]
            elif isinstance(d2.predicates[j], Formula) and d2.predicates[j].operation == '~' and isinstance(d1.predicates[i], Predicate):
                p1 = d1.predicates[i]
                p2 = d2.predicates[j].formulas[0]
            else:
                continue
            subst = unify_predicates(p1, p2)
            if not (subst is None):
                predicates1 = []
                for k in range(len(d1.predicates)):
                    if k != i:
                        predicates1.append(d1.predicates[k].copy())
                predicates2 = []
                for k in range(len(d2.predicates)):
                    if k != j:
                        predicates2.append(d2.predicates[k].copy())
                res = resolute_disjuncts(predicates1, predicates2, subst)
                # print(disjunct1, disjunct2)
                res[0].history = [disjunct1, disjunct2]
                new_disjuncts += res
    return new_disjuncts

class EmptyDisjunct:
    def __init__(self):
        self.history = []
    def __str__(self):
        return '[]'

class Disjunct:
    def __init__(self, *predicates):    # could be Formula('~', Predicate)
        self.predicates = list(predicates)
        self.history = []
    def __str__(self):
        str_preds = []
        for predicate in self.predicates:
            str_preds.append(str(predicate))
        return ' V '.join(str_preds)
    def has_negative(self):
        for predicate in self.predicates:
            if isinstance(predicate, Formula) and predicate.operation == '~':
                return True
    def collapse(self):
        new_disjuncts = []
        for i in range(len(self.predicates)):
            for j in range(i + 1, len(self.predicates)):
                p1 = self.predicates[i]
                p2 = self.predicates[j]
                subst = unify_predicates(p1, p2)
                if not (subst is None):
                    predicates = []
                    for k in range(len(self.predicates)):
                        if k != i and k != j:
                            predicates.append(self.predicates[k].copy())
                    new_disjuncts.append(collapse_disjunct(predicates, p1.copy(), p2.copy()))
                    new_disjuncts[-1].history = [self]
        new_new_disjuncts = []
        for disjunct in new_disjuncts:
            new_new_disjuncts += disjunct.collapse()
        return new_disjuncts + new_new_disjuncts

def output_history(disjunct):
    if len(disjunct.history) == 0:
        return str(disjunct)
    elif len(disjunct.history) == 1:
        print('Collapse', output_history(disjunct.history[0]), '=>', str(disjunct))
        return str(disjunct)
    elif len(disjunct.history) == 2:
        print('Resolution', output_history(disjunct.history[0]), 'and', output_history(disjunct.history[1]), '=>', str(disjunct))
        return str(disjunct)


class Disjunct_set:
    def __init__(self, *disjuncts):
        self.disjuncts = list(disjuncts)
    def __str__(self):
        str_disjs = []
        for disjunct in self.disjuncts:
            str_disjs.append(str(disjunct))
        return ', '.join(str_disjs)
    def collapse(self):
        new_disjuncts = []
        for disjunct in self.disjuncts:
            new_disjuncts += disjunct.collapse()
        self.disjuncts += new_disjuncts
    def separate(self): # by empty erbran interpretation
        self.T = []
        self.F = []
        for disjunct in self.disjuncts:
            if disjunct.has_negative():
                self.T.append(disjunct)
            else:
                self.F.append(disjunct)
    def make_resolutions(self): # I-resolution compute
        new_disjuncts = []
        for t in self.T:
            for f in self.F:
                new_disjuncts += resolution(t, f)
        self.disjuncts += new_disjuncts
    def has_empty_disjunct(self, output=False):
        for disjunct in self.disjuncts:
            if isinstance(disjunct, EmptyDisjunct):
                if output:
                    output_history(disjunct)
                    # for dis in self.disjuncts:
                    #     print(dis.history, [dis], dis)
                return True
        return False

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
        if predicate1.operation != '~' or not isinstance(predicate2, Formula) or predicate2.operation != '~' or not isinstance(predicate1.formulas[0], Predicate) or not isinstance(predicate2.formulas[0], Predicate):
            return None
        predicate1 = predicate1.formulas[0]
        predicate2 = predicate2.formulas[0]
    elif isinstance(predicate2, Formula):
        return None
    if predicate1.name != predicate2.name:
        return None
    eq_system = []
    for i in range(len(predicate1.args)):
        eq_system.append([predicate1.args[i], predicate2.args[i]])
    
    unified = False
    while not unified and len(eq_system) > 0:
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
            elif isinstance(curr_eq[0], Variable):
                if not curr_eq[1].contains(curr_eq[0]):
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
                else:
                    return None
            if changed:
                break
            eq_ind = (eq_ind + 1) % len(eq_system)
            if eq_ind == eq_ind_start:
                unified = True
                break
    for eq in eq_system:
        if isinstance(eq[0], Constant):
            return None
    return eq_system


def resolution_compute(disjunct_set: Disjunct_set, output=False):
    while True:
        disjunct_set.collapse()
        if disjunct_set.has_empty_disjunct(output):
            break
        disjunct_set.separate()
        disjunct_set.make_resolutions()
        if disjunct_set.has_empty_disjunct(output):
            break
    return True

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
        print('SNF conversion')
    formula.transform_to_SNF(dict(), [])
    if output:
        print('Transform to SNF:', str(formula))
    disjunction_set = extract_disjunct_set(formula)
    if output:
        print('Disjunction set:', str(disjunction_set))
        print('Resolution compute')
    resolution_compute(disjunction_set, output)
    return True