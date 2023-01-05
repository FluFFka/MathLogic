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
