import types
import webbrowser
from sympy import *
import math
import requests

desmos_symbols = {chr(i): chr(i) for i in range(65, 91)}
desmos_symbols.update({chr(i): chr(i) for i in range(97, 123)})
desmos_symbols.update({
    'alpha': r'\alpha',
    'nu': r'\nu',
    'beta': r'\beta',
    'xi': r'\xi',
    'Xi': r'\Xi',
    'gamma': r'\gamma',
    'Gamma': r'\Gamma',
    'delta': r'\delta',
    'Delta': r'\Delta',
    'pi': r'\pi',
    'Pi': r'\Pi',
    'epsilon': r'\epsilon',
    'varepsilon': r'\varepsilon',
    'rho': r'\rho',
    'varrho': r'\varrho',
    'zeta': r'\zeta',
    'sigma': r'\sigma',
    'Sigma': r'\Sigma',
    'eta': r'\eta',
    'tau': r'\tau',
    'theta': r'\theta',
    'vartheta': r'\vartheta',
    'Theta': r'\Theta',
    'upsilon': r'\upsilon',
    'Upsilon': r'\Upsilon',
    'iota': r'\iota',
    'phi': r'\phi',
    'varphi': r'\varphi',
    'Phi': r'\Phi',
    'kappa': r'\kappa',
    'chi': r'\chi',
    'lambda': r'\lambda',
    'psi': r'\psi',
    'Psi': r'\Psi',
    'mu': r'\mu',
    'omega': r'\omega',
    'Omega': r'\Omega',
    'ln': r'\ln',
})


def oeis_query(query):
    """returns a list of of the first OEIS sequence ids sorted by their relevance to the query"""
    query_text = ','.join(str(int(x)) for x in query) if isinstance(query, list) else repr(query)
    url = f'https://oeis.org/search?q={query_text}'
    raw = requests.get(url).text
    if 'Sorry, but the terms do not match anything in the table' in raw:
        raise ValueError('Sorry, but the terms do not match anything in the table')
    prefix = '/search?q=id:'
    sequences = []
    while prefix in raw:
        raw = raw[raw.index(prefix) + len(prefix):]
        sequence = raw[:7]
        sequences.append(sequence)
    return sequences


def oeis_sequence_id(value):
    """returns the most relevant valid OEIS sequence id from the given value"""
    def is_query(value):
        if isinstance(value, list):
            return True
        if isinstance(value, str):
            return not value.isdigit() and not (value.startswith('A') and value[1:].isdigit())

    if is_query(value):
        return oeis_query(value)[0]

    sequence = str(value)
    if sequence.startswith('A'):
        sequence = sequence[1:]

    return 'A' + sequence.zfill(6)


def oeis(sequence, max_terms=None):
    """returns a dictionary based on the most relevant OEIS sequence given by the input sequence"""

    sequence_id = oeis_sequence_id(sequence)[1:]

    raw = requests.get(f'https://oeis.org/A{sequence_id}/b{sequence_id}.txt').text

    if 'Sorry, the page you requested was not found' in raw:
        raise ValueError('Sorry, the page you requested was not found')

    def parse_raw(text):
        entries = {}
        for line in text.split('\n'):
            # print(line)
            index, value = None, None
            digits = ''
            for character in line + ' ':
                if character in '0123456789-':
                    digits += character
                elif character in '#':
                    break
                elif digits:
                    if index is None:
                        index = int(digits)
                        digits = ''
                    else:
                        value = int(digits)
                        break
            if value is not None:
                entries[index] = value
                if max_terms and len(entries) >= max_terms:
                    break
        return entries

    return parse_raw(raw)


class Variable(Symbol):
    """extension of the sympy Symbol class to allow for quick and dirty interaction with the desmos graph"""
    def __new__(cls, symbol, graph):
        obj = Symbol.__new__(cls, symbol)
        obj.graph = graph
        return obj

    def __xor__(self, other):
        return Variable(str(self) + "'" * other, self.graph)

    def __getitem__(self, item):
        return Variable('%s_{%s}' % (self, to_latex(item)), self.graph)

    def __setitem__(self, key, value):
        self.graph.eq(self(key), value)

    def __call__(self, *args):
        """returns a symbolic representation of a function call"""
        return Variable(f'{self}({", ".join(to_latex(arg) for arg in args)})', self.graph)


def to_latex(expression):
    """converts a sympy expression to latex, if it isn't already"""
    if isinstance(expression, str):
        for key, value in desmos_symbols.items():
            if key == value:
                continue
            if key in expression:
                expression = expression.replace(key, value).replace('\\\\', '\\')
        return expression
    if hasattr(expression, 'to_latex'):
        return expression.to_latex()
    try:
        return latex(expression)
    except:
        return str(expression)


def parse_dict(dict_, tabs=0):
    def parse(val):
        if isinstance(val, str):
            val = repr(val)
        elif isinstance(val, dict):
            val = parse_dict(val, tabs + 1)
        elif isinstance(val, list):
            val = f'[{", ".join(parse_dict(x, tabs + 1) for x in val)}]'
        elif isinstance(val, tuple):
            val = f'({", ".join(parse_dict(x, tabs + 1) for x in val)})'
        elif isinstance(val, bool):
            val = ['false', 'true'][int(val)]
        return val
    if not isinstance(dict_, dict):
        return parse(dict_)
    string = '{\n'
    for key, value in dict_.items():
        string += '\t' * (tabs + 1) + f'{key}: {parse(value)},\n'
    string += '\t' * tabs + '}'
    return string


class Graph:
    def __init__(self, graph_name='temp', api_key="dcb31709b452b1cf9dc26972add0fda6"):
        self.graph_name = graph_name
        self.file_name = graph_name + '.html'
        self.html = f'<body style="background-color:#2A2A2A;" marginwidth="0px" marginheight="0px">\n' \
                    f'<script src="https://www.desmos.com/api/v1.7/calculator.js?apiKey={api_key}"></script>\n' \
                    f'<div id="calculator"></div>\n' \
                    f'<script>\n' \
                    f'\tvar elt = document.getElementById("calculator");\n' \
                    f'\tvar calculator = Desmos.GraphingCalculator(elt);\n'
        self.expression_count = 0
        self.A, self.B, self.C = Variable('A', self), Variable('B', self), Variable('C', self)
        self.D, self.E, self.F = Variable('D', self), Variable('E', self), Variable('F', self)
        self.G, self.H, self.I = Variable('G', self), Variable('H', self), Variable('I', self)
        self.J, self.K, self.L = Variable('J', self), Variable('K', self), Variable('L', self)
        self.M, self.N, self.O = Variable('M', self), Variable('N', self), Variable('O', self)
        self.P, self.Q, self.R = Variable('P', self), Variable('Q', self), Variable('R', self)
        self.S, self.T, self.U = Variable('S', self), Variable('T', self), Variable('U', self)
        self.V, self.W, self.X = Variable('V', self), Variable('W', self), Variable('X', self)
        self.Y, self.Z, self.a = Variable('Y', self), Variable('Z', self), Variable('a', self)
        self.b, self.c, self.d = Variable('b', self), Variable('c', self), Variable('d', self)
        self.e, self.f, self.g = Variable('e', self), Variable('f', self), Variable('g', self)
        self.h, self.i, self.j = Variable('h', self), Variable('i', self), Variable('j', self)
        self.k, self.l, self.m = Variable('k', self), Variable('l', self), Variable('m', self)
        self.n, self.o, self.p = Variable('n', self), Variable('o', self), Variable('p', self)
        self.q, self.r, self.s = Variable('q', self), Variable('r', self), Variable('s', self)
        self.t, self.u, self.v = Variable('t', self), Variable('u', self), Variable('v', self)
        self.w, self.x, self.y = Variable('w', self), Variable('x', self), Variable('y', self)
        self.z = Variable('z', self)
        self.alpha, self.nu, self.beta = Variable(r'\alpha', self), Variable(r'\nu', self), Variable(r'\beta', self)
        self.xi, self.Xi, self.gamma = Variable(r'\xi', self), Variable(r'\Xi', self), Variable(r'\gamma', self)
        self.Gamma, self.delta = Variable(r'\Gamma', self), Variable(r'\delta', self)
        self.Delta, self.pi, self.Pi = Variable(r'\Delta', self), Variable(r'\pi', self), Variable(r'\Pi', self)
        self.epsilon, self.varepsilon = Variable(r'\epsilon', self), Variable(r'\varepsilon', self)
        self.rho, self.varrho = Variable(r'\rho', self), Variable(r'\varrho', self)
        self.zeta, self.sigma = Variable(r'\zeta', self), Variable(r'\sigma', self)
        self.Sigma, self.eta, self.tau = Variable(r'\Sigma', self), Variable(r'\eta', self), Variable(r'\tau', self)
        self.theta, self.vartheta = Variable(r'\theta', self), Variable(r'\vartheta', self)
        self.Theta, self.upsilon = Variable(r'\Theta', self), Variable(r'\upsilon', self)
        self.Upsilon, self.iota = Variable(r'\Upsilon', self), Variable(r'\iota', self)
        self.phi, self.varphi, self.Phi = Variable(r'\phi', self), Variable(r'\varphi', self), Variable(r'\Phi', self)
        self.kappa, self.chi = Variable(r'\kappa', self), Variable(r'\chi', self)
        self.lambda_, self.psi, self.Psi = Variable(r'\lambda', self), Variable(r'\psi', self), Variable(r'\Psi', self)
        self.mu, self.omega, self.Omega = Variable(r'\mu', self), Variable(r'\omega', self), Variable(r'\Omega', self)
        self.ln = Variable(r'\ln', self)

    def set_expression(self, **kwargs):
        """based on desmos api v1.7"""
        if 'id' not in kwargs:
            kwargs['id'] = str(self.expression_count)
            self.expression_count += 1
        self.html += f'\tcalculator.setExpression({parse_dict(kwargs, 1)});\n'

    def append(self, value, **kwargs):
        self.set_expression(latex=to_latex(value), **kwargs)

    def define(self, lhs, rhs, relation='=', **kwargs):
        self.set_expression(latex=f'{to_latex(lhs)}{relation}{to_latex(rhs)}', **kwargs)

    def __setitem__(self, lhs, rhs):
        self.define(lhs, rhs)

    def eq(self, lhs, rhs, **kwargs):
        self.define(lhs, rhs, '=', **kwargs)

    def lt(self, lhs, rhs, **kwargs):
        self.define(lhs, rhs, '<', **kwargs)

    def le(self, lhs, rhs, **kwargs):
        self.define(lhs, rhs, r'\le ', **kwargs)

    def gt(self, lhs, rhs, **kwargs):
        self.define(lhs, rhs, '>', **kwargs)

    def ge(self, lhs, rhs, **kwargs):
        self.define(lhs, rhs, r'\ge ', **kwargs)

    def new_slider(self, symbol, initial_value=1, min=-10, max=10, step='""', **kwargs):
        kwargs.update({'sliderBounds': {'min': to_latex(min), 'max': to_latex(max), 'step': to_latex(step)}})
        self.define(symbol, initial_value, **kwargs)

    def new_table(self, columns, **kwargs):
        new_columns = []
        for latex, values in columns.items():
            column = {'latex': to_latex(latex)}
            if values:
                column['values'] = [to_latex(x) for x in values]
            column.update(kwargs)
            new_columns.append(column)
        self.set_expression(**{'type': 'table', 'columns': new_columns})

    def save(self):
        with open(self.file_name, 'w') as html_file:
            html_file.write(self.html + '</script>')

    def open(self):
        self.save()
        webbrowser.open(self.file_name, new = 0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.open()

    def __call__(self, *args, **kwargs):
        slider_kwargs = ['min', 'max', 'step']
        special_kwargs = ['type', 'latex', 'color', 'lineStyle', 'lineWidth', 'lineOpacity', 'pointStyle',
                          'pointSize', 'pointOpacity', 'fillOpacity', 'points', 'lines', 'fill', 'hidden', 'secret',
                          'sliderBounds', 'parametricDomain', 'polarDomain', 'id', 'dragMode', 'label', 'showLabel',
                          'labelSize', 'labelOrientation']
        non_special_kwargs = {key: value for key, value in kwargs.items() if key not in slider_kwargs + special_kwargs}
        kwargs = {key: value for key, value in kwargs.items() if key in slider_kwargs + special_kwargs}
        if non_special_kwargs:
            if isinstance(list(non_special_kwargs.values())[0], list):
                self(non_special_kwargs, **kwargs)
            else:
                for lhs, rhs in non_special_kwargs.items():
                    self(lhs, rhs, **kwargs)
        elif any(key in slider_kwargs for key, value in kwargs.items()):
            if callable(args[0]) and (args[0].__name__ == "<lambda>" or isinstance(args[0], types.FunctionType)):
                self.plot_function(*args, **kwargs)
            else:
                self.new_slider(*args, **kwargs)
        elif len(args) == 1:
            if isinstance(args[0], dict):
                self.new_table(args[0], **kwargs)
            else:
                self.append(args[0], **kwargs)
        elif len(args) == 2:
            self.define(args[0], args[1], **kwargs)
        else:
            self.append(' '.join(to_latex(arg) for arg in args), **kwargs)

    def plot_function(self, function, min, max, step=1, independent_variable='x', dependent_variable='y', **kwargs):
        N = math.ceil((max - min) / step)
        X = [min + step * n for n in range(int(N))]
        Y = [function(x) for x in X]
        self.new_table({independent_variable: X, dependent_variable: Y}, **kwargs)

    def plot_oeis(self, sequence, max_terms=None, **kwargs):
        sequence_id = oeis_sequence_id(sequence)[1:]
        n, A = zip(*oeis(sequence_id, max_terms).items())
        self.new_table({'n_{%d}' % int(sequence_id): n, 'A_{%d}' % int(sequence_id): A}, **kwargs)

    def __or__(self, other):
        self.__call__(other)
