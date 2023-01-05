import SemanticTableaux

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
    # 'Ex P(x) & Ex ~P(x)'
]

for formula_str in formulas_str:
    parsed_formula_str = str(SemanticTableaux.str_to_formula(formula_str))
    print(f'Formula {parsed_formula_str} is valid?', SemanticTableaux.is_valid_formula(formula_str, output=True))
    print()