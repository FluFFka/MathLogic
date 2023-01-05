from Formulas import *

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
    # formula.move_quantifiers()
    # if output:
    #     print('Move quantifiers:', str(formula))
    return True