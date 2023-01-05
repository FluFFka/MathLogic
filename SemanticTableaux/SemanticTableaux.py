indent = '    '

class Constant:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __eq__(self, other):
        if not isinstance(other, Constant):
            return False
        return self.name == other.name
    def copy(self):
        return Constant(self.name)
    def __hash__(self):
        return hash(self.name)

const__ = -1
def nextConst():
    global const__
    const__ += 1
    return Constant('c' + str(const__))
start_const = nextConst()


class Variable:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return self.name == other.name
    def copy(self):
        return Variable(self.name)


class Predicate:
    def __init__(self, name, *args):
        self.name = name
        self.args = list(args)
    def __str__(self):
        res = self.name + '('
        str_args = []
        for arg in self.args:
            str_args.append(str(arg))
        res += ','.join(str_args)
        res += ')'
        return res
    def __eq__(self, other):
        if not isinstance(other, Predicate):
            return False
        if self.name != other.name:
            return False
        if len(self.args) != len(other.args):
            return False
        for i in range(len(self.args)):
            if self.args[i] != other.args[i]:
                return False
        return True
    def put_term(self, varname, term):
        for i in range(len(self.args)):
            if isinstance(self.args[i], Variable) and self.args[i].name == varname:
                self.args[i] = term
    def get_consts(self):
        consts = []
        for arg in self.args:
            if isinstance(arg, Constant):
                consts.append(arg)
        return list(set(consts))
    def copy(self):
        copies = []
        for arg in self.args:
            copies.append(arg.copy())
        return Predicate(self.name, *copies)


class Formula:
    def __init__(self, operation, *formulas):        
        self.operation = operation
        self.formulas = list(formulas)
    def __str__(self):
        str_formulas = []
        for formula in self.formulas:
            str_formulas.append(str(formula))
        if len(str_formulas) == 1:
            res = self.operation[::-1] + '(' + str_formulas[0] + ')'
        elif len(str_formulas) == 2:
            if self.operation == '>':
                res = '(' + str_formulas[0] + ' -> ' + str_formulas[1] + ')'
            else:
                res = '(' + str_formulas[0] + ' ' + self.operation + ' ' + str_formulas[1] + ')'
        return res
    def put_term(self, varname, term):
        if self.operation[0] == varname:
            return
        for formula in self.formulas:
            formula.put_term(varname, term)
    def get_consts(self):
        consts = []
        for formula in self.formulas:
            if len(formula.get_consts()):
                consts += formula.get_consts()
        return list(set(consts))
    def copy(self):
        copies = []
        for formula in self.formulas:
            copies.append(formula.copy())
        return Formula(self.operation, *copies)

def isbinary(sym: str):
    return sym in ('V', '&', '>')

def isunary(sym: str):
    return sym[-1] in ('A', 'E', '~')

def isQuantifier(sym: str):
    return sym[-1] in ('A', 'E')

def isOperatorQuantifier(sym: str):
    return sym in ('~', '&', 'V', '>') or sym[-1] in ('A', 'E')

def priority(sym: str):
    priorities = {'~': 0, '&': 1, 'V': 2, '>': 3}
    if sym in priorities:
        return priorities[sym]
    elif sym[-1] in ('A', 'E'):
        return 0
    print('Error in formula')
    exit(1)

def ispredicate(sym: str):
    return sym.isupper() and not (sym in ('A', 'E', 'V'))

def isvariable(sym: str):
    return sym.islower()

def str_to_reverse_polish_notation(string: str):
    string = string.replace(' ', '').replace('->', '>')
    stack = ['#']
    curr_ind = 0
    out_queue = []
    while curr_ind < len(string):
        if string[curr_ind] in ('A', 'E'):
            stack.append(string[curr_ind])
        elif isvariable(string[curr_ind]):
            if stack[-1] in ('A', 'E'):
                stack[-1] = string[curr_ind] + stack[-1]
            else:
                out_queue.append(string[curr_ind])
        elif ispredicate(string[curr_ind]):
            stack.append(string[curr_ind])
        elif string[curr_ind] == ',':
            while stack[-1] != '(':
                sym = stack.pop()
                out_queue.append(sym)
                if stack[-1] == '#':
                    print('Missed bracket or comma')
                    exit(1)
        elif isOperatorQuantifier(string[curr_ind]):
            while isOperatorQuantifier(stack[-1]) and priority(stack[-1]) < priority(string[curr_ind]):
                sym = stack.pop()
                out_queue.append(sym)
            stack.append(string[curr_ind])
        elif string[curr_ind] == '(':
            stack.append('(')
        elif string[curr_ind] == ')':
            while stack[-1] != '(':
                sym = stack.pop()
                out_queue.append(sym)
                if stack[-1] == '#':
                    print('Missed bracket')
                    exit(1)
            stack.pop()
            if ispredicate(stack[-1]):
                sym = stack.pop()
                out_queue.append(sym)
        curr_ind += 1
    while stack[-1] != '#':
        if stack[-1] == '(':
            print('Missed bracket')
        sym = stack.pop()
        out_queue.append(sym)
    return out_queue

def str_to_formula(string: str):
    queue = str_to_reverse_polish_notation(string)
    stack = ['#']
    for sym in queue:
        if isvariable(sym): # Const
            stack.append(Variable(sym))
        elif isQuantifier(sym):
            pp = stack.pop()
            stack.append(Formula(sym, pp))
        elif isunary(sym):
            pp = stack.pop()
            stack.append(Formula(sym, pp))
        elif isbinary(sym):
            pp2 = stack.pop()
            pp1 = stack.pop()
            stack.append(Formula(sym, pp1, pp2))
        else:
            name = sym
            arguments = []
            while isinstance(stack[-1], Variable):  # Const
                pp = stack.pop()
                arguments.append(pp)
            stack.append(Predicate(name, *arguments[::-1]))
    if len(stack) != 2:
        print('Wrong stack size')
        exit(1)
    return stack[-1]

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
            in_formula.put_term(formula.operation[0], nextConst())
            new_st = SemanticTableaux(st.T + [in_formula], st.F, st.closedT, st.closedF, st.order + [True])
            return compute(new_st, ind+1, output)
        elif formula.operation[-1] == 'A':
            extra_orders = []
            extra_T = []
            for const in consts:
                extra_orders.append(True)
                in_formula = formula.formulas[0].copy()
                in_formula.put_term(formula.operation[0], const)
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
            in_formula.put_term(formula.operation[0], nextConst())
            new_st = SemanticTableaux(st.T, st.F + [in_formula], st.closedT, st.closedF, st.order + [False])
            return compute(new_st, ind+1, output)
        elif formula.operation[-1] == 'E':
            extra_orders = []
            extra_F = []
            for const in consts:
                extra_orders.append(False)
                in_formula = formula.formulas[0].copy()
                in_formula.put_term(formula.operation[0], const)
                extra_F.append(in_formula)
            extra_F.append(formula)
            extra_orders.append(False)
            new_st = SemanticTableaux(st.T, st.F + extra_F, st.closedT, st.closedF, st.order + extra_orders)
            return compute(new_st, ind+1, output)
        
def is_valid_formula(string: str, output=False):
    formula = str_to_formula(string)
    return compute(SemanticTableaux([], [formula]), output=output)
