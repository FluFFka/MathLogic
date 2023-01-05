indent = '    '
available_functionals = ['f', 'g', 'h']

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
    def rename_variables(self, names, name_suffixes):
        pass    # no variables

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
    def rename_variables(self, names, name_suffixes):
        if self.name in names:
            self.name = names[self.name]


class Functional:
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
        if not isinstance(other, Functional):
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
            elif isinstance(self.args[i], Functional):
                self.args[i].put_term(varname, term)
    def get_consts(self):
        consts = []
        for arg in self.args:
            if isinstance(arg, Constant):
                consts.append(arg)
            elif isinstance(arg, Functional):
                consts += arg.get_consts()
        return list(set(consts))
    def copy(self):
        copies = []
        for arg in self.args:
            copies.append(arg.copy())
        return Functional(self.name, *copies)
    def rename_variables(self, names, name_suffixes):
        for arg in self.args:
            arg.rename_variables(names, name_suffixes)

func__ = -1
def nextFunctional(args):
    global func__
    func__ += 1
    return Functional('f' + str(func__), *args)


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
            elif isinstance(self.args[i], Functional):
                self.args[i].put_term(varname, term)
    def get_consts(self):
        consts = []
        for arg in self.args:
            if isinstance(arg, Constant):
                consts.append(arg)
            elif isinstance(arg, Functional):
                consts += arg.get_consts()
        return list(set(consts))
    def copy(self):
        copies = []
        for arg in self.args:
            copies.append(arg.copy())
        return Predicate(self.name, *copies)
    def rename_variables(self, names, name_suffixes):
        for arg in self.args:
            arg.rename_variables(names, name_suffixes)


class Formula:
    def __init__(self, operation, *formulas):
        self.operation = operation
        self.formulas = list(formulas)
    def __str__(self):
        str_formulas = []
        for formula in self.formulas:
            str_formulas.append(str(formula))
        if len(str_formulas) == 1:
            res = self.operation[-1] + self.operation[:-1] + '(' + str_formulas[0] + ')'
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
    def rename_variables(self, names, name_suffixes):
        if self.operation[-1] in ('A', 'E'):
            varname = self.operation[:-1]
            if names.get(varname) is None:
                if name_suffixes.get(varname) is None:
                    name_suffixes[varname] = 0
                else:
                    name_suffixes[varname] += 1
                names[varname] = varname + str(name_suffixes[varname])
            else:
                name_suffixes[varname] += 1
            names[varname] = varname + str(name_suffixes[varname])
            self.operation = names[varname] + self.operation[-1]
        for formula in self.formulas:
            formula.rename_variables(names.copy(), name_suffixes)
    def remove_implications(self):
        if self.operation == '>':
            self.operation = 'V'
            self.formulas[0] = Formula('~', self.formulas[0])
        for formula in self.formulas:
            if isinstance(formula, Formula):
                formula.remove_implications()
    def move_negations(self):
        if self.operation == '~' and isinstance(self.formulas[0], Formula):
            in_formula = self.formulas[0]
            if in_formula.operation == '&':
                self.operation = 'V'
                self.formulas = [None, None]
                self.formulas[0] = Formula('~', in_formula.formulas[0])
                self.formulas[1] = Formula('~', in_formula.formulas[1])
            elif in_formula.operation == 'V':
                self.operation = '&'
                self.formulas = [None, None]
                self.formulas[0] = Formula('~', in_formula.formulas[0])
                self.formulas[1] = Formula('~', in_formula.formulas[1])
            elif in_formula.operation[-1] == 'E':
                self.operation, in_formula.operation = in_formula.operation, self.operation
                self.operation = self.operation[:-1] + 'A'
            elif in_formula.operation[-1] == 'A':
                self.operation, in_formula.operation = in_formula.operation, self.operation
                self.operation = self.operation[:-1] + 'E'
        for i in range(len(self.formulas)):
            check_double_negation = True
            while check_double_negation:
                in_formula = self.formulas[i]
                if isinstance(in_formula, Formula) and in_formula.operation == '~':
                    in_in_formula = in_formula.formulas[0]
                    if isinstance(in_in_formula, Formula) and in_in_formula.operation == '~':
                        self.formulas[i] = in_in_formula.formulas[0]
                    else:
                        check_double_negation = False
                else:
                    check_double_negation = False
        for formula in self.formulas:
            if isinstance(formula, Formula):
                formula.move_negations()
    def move_quantifiers(self):
        for formula in self.formulas:
            if isinstance(formula, Formula):
                formula.move_quantifiers()
        if self.operation in ('V', '&'):
            if isinstance(self.formulas[0], Formula) and self.formulas[0].operation[-1] in ('A', 'E'):
                in_formula = self.formulas[0]
                self.operation, in_formula.operation = in_formula.operation, self.operation
                self.formulas, in_formula.formulas = [in_formula], [in_formula.formulas[0], self.formulas[1]]
                in_formula.move_quantifiers()
            elif isinstance(self.formulas[1], Formula) and self.formulas[1].operation[-1] in ('A', 'E'):
                in_formula = self.formulas[1]
                self.operation, in_formula.operation = in_formula.operation, self.operation
                self.formulas, in_formula.formulas = [in_formula], [self.formulas[0], in_formula.formulas[0]]
                in_formula.move_quantifiers()
    def transform_to_CNF(self):
        for formula in self.formulas:
            if isinstance(formula, Formula):
                formula.transform_to_CNF()
        if self.operation == 'V':
            if isinstance(self.formulas[0], Formula) and self.formulas[0].operation == '&':
                left1 = self.formulas[0].formulas[0]
                left2 = self.formulas[0].formulas[1]
                right = self.formulas[1]
                self.operation = '&'
                self.formulas = [Formula('V', left1, right), Formula('V', left2, right.copy())]
                self.formulas[0].transform_to_CNF()
                self.formulas[1].transform_to_CNF()
            elif isinstance(self.formulas[1], Formula) and self.formulas[1].operation == '&':
                left = self.formulas[0]
                right1 = self.formulas[1].formulas[0]
                right2 = self.formulas[1].formulas[1]
                self.operation = '&'
                self.formulas = [Formula('V', left, right1), Formula('V', left.copy(), right2)]
                self.formulas[0].transform_to_CNF()
                self.formulas[1].transform_to_CNF()
    def transform_to_SNF(self, names, variables):
        if self.operation[-1] == 'A':
            variables.append(self.operation[:-1])
            self.formulas[0].transform_to_SNF(names, variables)
        elif self.operation[-1] == 'E':
            names[self.operation[:-1]] = nextFunctional(variables)
            self.formulas[0].transform_to_SNF(names, variables)
            self.operation = self.formulas[0].operation
            self.formulas = self.formulas[0].formulas
        else:
            for formula in self.formulas:
                if isinstance(formula, Predicate):
                    for name, term in names.items():
                        formula.put_term(name, term)
                else:
                    formula.transform_to_SNF(names, variables)

            
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

def isfunctional(sym: str):
    return sym[-1] in available_functionals

def ispredicate(sym: str):
    return sym.isupper() and not (sym in ('A', 'E', 'V'))

def isvariable(sym: str):
    return sym.islower() and not isfunctional(sym)

def str_to_reverse_polish_notation(string: str):
    string = string.replace(' ', '').replace('->', '>')
    stack = ['#']
    curr_ind = 0
    out_queue = []
    comma_stack = ['#']
    while curr_ind < len(string):
        if string[curr_ind] in ('A', 'E'):
            stack.append(string[curr_ind])
        elif isvariable(string[curr_ind]):
            if stack[-1] in ('A', 'E'):
                stack[-1] = string[curr_ind] + stack[-1]
            else:
                out_queue.append(string[curr_ind])
        elif ispredicate(string[curr_ind]) or isfunctional(string[curr_ind]):
            comma_stack.append(0)
            stack.append(string[curr_ind])
        elif string[curr_ind] == ',':
            comma_stack[-1] += 1
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
                comma_stack.pop()
                out_queue.append(sym)
            elif isfunctional(stack[-1]):
                sym = stack.pop()
                argnum = comma_stack.pop() + 1
                sym = str(argnum) + sym
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
        elif ispredicate(sym):
            name = sym
            arguments = []
            while isinstance(stack[-1], Variable) or isinstance(stack[-1], Functional) or isinstance(stack[-1], Constant):
                pp = stack.pop()
                arguments.append(pp)
            stack.append(Predicate(name, *arguments[::-1]))
        elif isfunctional(sym):
            name = sym[-1]
            argnum = int(sym[:-1])
            arguments = []
            while (isinstance(stack[-1], Variable) or isinstance(stack[-1], Functional) or isinstance(stack[-1], Constant)) and (argnum > 0):
                argnum -= 1
                pp = stack.pop()
                arguments.append(pp)
            stack.append(Functional(name, *arguments[::-1]))
        else:
            print('Wrong symbols in input')
            exit(1)
        
    if len(stack) != 2:
        print('Wrong stack size')
        exit(1)
    return stack[-1]
