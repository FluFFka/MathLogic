from Formulas import *

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