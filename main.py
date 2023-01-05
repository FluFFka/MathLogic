from Formulas import *
from SemanticTableaux import *
from ResolutionMethod import *

formulas_str = [
    # 'Ex P(x) -> ~Ax ~P(x)',
    # 'ExAy R(x,y) -> AyEx R(x,y)',
    # 'Ax (P(x) -> Ey R(x, y)) -> (Ex ~P(x) V AxEzR(x, z))',
    # 'Ax Ey Az (P(x, y) -> P(y, z))',
    # 'Ex Ay Ez (P(x, y) -> P(y, z))',
    # 'Ax (P(x)&R(x)) -> (Ax P(x) & Ax R(x))',
    # '(Ax P(x) & Ax R(x)) -> Ax (P(x)&R(x))',
    # 'Ex (P(x) V R(x)) -> (Ex P(x) V Ex R(x))',
    # '(Ex P(x) V Ex R(x)) -> Ex (P(x) V R(x))',
    # '(Ax P(x) V R(y)) -> Ax (P(x) V R(y))',
    # 'Ax (P(x) V R(y)) -> (Ax P(x) V R(y))',
    # 'Ey Ax Q(x, y) -> Ax Ey Q(x, y)',
    # '~AxEy(G(x)VH(y))->Ey~(Ey~G(y)->H(y))',
    # 'Ax P(f(x, y), g(z), a, h(q, w, e))',
    # 'AxAx(AxP(x) & P(x) V ExQ(x) V Q(x))',
    'Ex (P(x) &(Ax P(x) ->Ey R(x, y)) -> Ey R(x, y))',
]

for formula_str in formulas_str:
    formula = str_to_formula(formula_str)
    # print(f'Formula {str(formula)} is valid?', semantic_tableaux_method(formula, output=False))
    # print(f'Formula {str(formula)} is valid?', semantic_tableaux_method(formula, output=False))
    resolution_method(formula, output=True)
    # print(f'Formula {str(formula)} is valid?', resolution_method(formula, output=True))
