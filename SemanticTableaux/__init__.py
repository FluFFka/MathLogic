from Formulas import *

class SemanticTableaux:
    def __init__(self, T, F, closedT=[], closedF=[], order=None):
        if order == None:
            self.T = T
            self.F = F
            self.closedT = closedT.copy()
            self.closedF = closedF.copy()
            self.order = [True for i in range(len(T))] + [False for j in range(len(T), len(T) + len(F))]
            return
        self.T = []
        self.F = []
        self.closedT = closedT.copy()
        self.closedF = closedF.copy()
        self.order = []
        
        t_ind = 0
        f_ind = 0
        for i in range(len(order)):
            if order[i]:
                if isinstance(T[t_ind], Predicate):
                    self.closedT.append(T[t_ind])
                else:
                    self.T.append(T[t_ind])
                    self.order.append(True)
                t_ind += 1
            else:
                if isinstance(F[f_ind], Predicate):
                    self.closedF.append(F[f_ind])
                else:
                    self.F.append(F[f_ind])
                    self.order.append(False)
                f_ind += 1

    def isclosed(self, ind=None, output=False):
        for t in self.closedT:
            for f in self.closedF:
                if t == f:
                    if not (ind is None) and output:
                        print(ind * indent, 'same: ', str(t), sep='')
                    return True
        return False

    def get_consts(self):
        consts = []
        for formula in self.T:
            consts += formula.get_consts()
        for formula in self.F:
            consts += formula.get_consts()
        for formula in self.closedT:
            consts += formula.get_consts()
        for formula in self.closedF:
            consts += formula.get_consts()
        return list(set(consts))

    def __str__(self):
        res = '< '
        str_T = []
        str_F = []
        for t in self.T:
            str_T.append(str(t))
        for t in self.closedT:
            str_T.append(str(t))
        for f in self.F:
            str_F.append(str(f))
        for f in self.closedF:
            str_F.append(str(f))
        res += ', '.join(str_T)
        res += ' | '
        res += ', '.join(str_F)
        res += ' >'
        return res

def compute(st: SemanticTableaux, ind=0, output=False):
    if output:
        print(ind * indent, str(st), sep='')
    if st.isclosed(ind, output):
        return True
    if len(st.order) == 0:
        return False
    if st.order[0]:
        consts = st.get_consts()
        if not consts:
            consts = [start_const]
        formula = st.T[0]
        if output:
            if formula.operation == '>':
                print(ind * indent, 'L', '->', ' for ', str(formula), sep='')
            else:
                print(ind * indent, 'L', formula.operation[-1], ' for ', str(formula), sep='')
        st.T = st.T[1:]
        st.order = st.order[1:]
        if formula.operation == '&':
            new_st = SemanticTableaux(st.T + formula.formulas, st.F, st.closedT, st.closedF, st.order + [True, True])
            return compute(new_st, ind+1, output)
        elif formula.operation == 'V':
            new_st1 = SemanticTableaux(st.T + [formula.formulas[0]], st.F, st.closedT, st.closedF, st.order + [True])
            new_st2 = SemanticTableaux(st.T + [formula.formulas[1]], st.F, st.closedT, st.closedF, st.order + [True])
            return compute(new_st1, ind+1, output) and compute(new_st2, ind+1, output)
        elif formula.operation == '>':
            new_st1 = SemanticTableaux(st.T + [formula.formulas[1]], st.F, st.closedT, st.closedF, st.order + [True])
            new_st2 = SemanticTableaux(st.T, st.F + [formula.formulas[0]], st.closedT, st.closedF, st.order + [False])
            return compute(new_st1, ind+1, output) and compute(new_st2, ind+1, output)
        elif formula.operation == '~':
            new_st = SemanticTableaux(st.T, st.F + formula.formulas, st.closedT, st.closedF, st.order + [False])
            return compute(new_st, ind+1, output)
        elif formula.operation[-1] == 'E':
            in_formula = formula.formulas[0].copy()
            in_formula.put_term(formula.operation[:-1], nextConst())
            new_st = SemanticTableaux(st.T + [in_formula], st.F, st.closedT, st.closedF, st.order + [True])
            return compute(new_st, ind+1, output)
        elif formula.operation[-1] == 'A':
            extra_orders = []
            extra_T = []
            for const in consts:
                extra_orders.append(True)
                in_formula = formula.formulas[0].copy()
                in_formula.put_term(formula.operation[:-1], const)
                extra_T.append(in_formula)
            extra_T.append(formula)
            extra_orders.append(True)
            new_st = SemanticTableaux(st.T + extra_T, st.F, st.closedT, st.closedF, st.order + extra_orders)
            return compute(new_st, ind+1, output)
    else:
        consts = st.get_consts()
        if not consts:
            consts = [start_const]
        formula = st.F[0]
        if output:
            if formula.operation == '>':
                print(ind * indent, 'R', '->', ' for ', str(formula), sep='')
            else:
                print(ind * indent, 'R', formula.operation[-1], ' for ', str(formula), sep='')
        st.F = st.F[1:]
        st.order = st.order[1:]
        if formula.operation == '&':
            new_st1 = SemanticTableaux(st.T, st.F + [formula.formulas[0]], st.closedT, st.closedF, st.order + [False])
            new_st2 = SemanticTableaux(st.T, st.F + [formula.formulas[1]], st.closedT, st.closedF, st.order + [False])
            return compute(new_st1, ind+1, output) and compute(new_st2, ind+1, output)
        elif formula.operation == 'V':
            new_st = SemanticTableaux(st.T, st.F + formula.formulas, st.closedT, st.closedF, st.order + [False, False])
            return compute(new_st, ind+1, output)
        elif formula.operation == '>':
            new_st = SemanticTableaux(st.T + [formula.formulas[0]], st.F + [formula.formulas[1]], st.closedT, st.closedF, st.order + [True, False])
            return compute(new_st, ind+1, output)
        elif formula.operation == '~':
            new_st = SemanticTableaux(st.T + formula.formulas, st.F, st.closedT, st.closedF, st.order + [True])
            return compute(new_st, ind+1, output)
        elif formula.operation[-1] == 'A':
            in_formula = formula.formulas[0].copy()
            in_formula.put_term(formula.operation[:-1], nextConst())
            new_st = SemanticTableaux(st.T, st.F + [in_formula], st.closedT, st.closedF, st.order + [False])
            return compute(new_st, ind+1, output)
        elif formula.operation[-1] == 'E':
            extra_orders = []
            extra_F = []
            for const in consts:
                extra_orders.append(False)
                in_formula = formula.formulas[0].copy()
                in_formula.put_term(formula.operation[:-1], const)
                extra_F.append(in_formula)
            extra_F.append(formula)
            extra_orders.append(False)
            new_st = SemanticTableaux(st.T, st.F + extra_F, st.closedT, st.closedF, st.order + extra_orders)
            return compute(new_st, ind+1, output)
    return False


def semantic_tableaux_method(formula: Formula, output=False):
    return compute(SemanticTableaux([], [formula]), output=output)
