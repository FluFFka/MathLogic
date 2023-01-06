from Formulas import *
from SemanticTableaux import *
from ResolutionMethod import *

formulas_str_tables = [
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

formulas_str_resolution = [
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
    'Ax (P(x) -> Ey R(x, f(y))) -> (Ex ~P(x) V AxEzR(x, z))',
    'ExAy(Az(P(y, z) -> P(x, z)) -> (P(x, x) -> P(y, x)))',
]


print('Semantic Tableaux method\n')
for formula_str in formulas_str_tables:
    formula = str_to_formula(formula_str)
    print('Formula:', str(formula))
    print(f'Formula {str(formula)} is valid?', semantic_tableaux_method(formula, output=False))
    print()
print('Resolution method\n')
for formula_str in formulas_str_tables:
    formula = str_to_formula(formula_str)
    print('Formula:', str(formula))
    print(f'Formula {str(formula)} is valid?', resolution_method(formula, output=True))
    print()