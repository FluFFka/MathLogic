from Formulas import *
from SemanticTableaux import *
from ResolutionMethod import *

formulas_str = [
    'Ex P(x) -> ~Ax ~P(x)',
    'ExAy R(x,y) -> AyEx R(x,y)',
    'Ax (P(x) -> Ey R(x, y)) -> (Ex ~P(x) V AxEzR(x, z))',
    'Ax Ey Az (P(x, y) -> P(y, z))',
    'Ex Ay Ez (P(x, y) -> P(y, z))',
    'Ax (P(x)&R(x)) -> (Ax P(x) & Ax R(x))',
    '(Ax P(x) & Ax R(x)) -> Ax (P(x)&R(x))',
    'Ex (P(x) V R(x)) -> (Ex P(x) V Ex R(x))',
    '(Ex P(x) V Ex R(x)) -> Ex (P(x) V R(x))',
    '(Ax P(x) V R(y)) -> Ax (P(x) V R(y))',
    'Ax (P(x) V R(y)) -> (Ax P(x) V R(y))',
    'Ey Ax Q(x, y) -> Ax Ey Q(x, y)',
    '~AxEy(G(x)VH(y))->Ey~(Ey~G(y)->H(y))',
    'Ex (P(x) &(Ax P(x) ->Ey R(x, y)) -> Ey R(x, y))',
]

for formula_str in formulas_str:
    formula = str_to_formula(formula_str)
    # print(f'Formula {str(formula)} is valid?', semantic_tableaux_method(formula, output=False))
    # print(f'Formula {str(formula)} is valid?', semantic_tableaux_method(formula, output=False))
    print(f'Formula {str(formula)} is valid?', resolution_method(formula, output=False))
    # print(f'Formula {str(formula)} is valid?', resolution_method(formula, output=True))


# p1 = Predicate('P', Functional('f', Variable('x'), Variable('y')), Variable('z'), Functional('h', Variable('z'), Variable('y')))
# p2 = Predicate('P', Functional('f', Variable('y'), Variable('x')), Functional('g', Variable('y')), Variable('v'))
# p1 = Predicate('P', Functional('f', Variable('x'), Functional('g', Variable('y'))), Constant('c'))
# p2 = Predicate('P', Functional('f', Functional('g', Variable('y')), Variable('x')), Variable('y'))
# print(str(p1))
# print(str(p2))
# subst = unify_predicates(p1, p2)
# for eq in subst:
#     print(str(eq[0]), str(eq[1]))
# p1.put_terms(subst)
# p2.put_terms(subst)
# print(str(p1))
# print(str(p2))

# f1 = Formula('V', Predicate('P', Variable('x')), Predicate('P', Variable('x')))
# print(str(f1))
# ds1 = extract_disjunct_set(f1)
# print('ds1:', str(ds1))
# ds1.collapse()
# print('ds1:', str(ds1))

# f1 = Formula('~', Predicate('R', Variable('x'), Variable('y')))
# f2 = Predicate('R', Variable('z'), Functional('f', 'a'))
# print(str(f1))
# print(str(f2))
# print(unify_predicates(f1.formulas[0], f2))