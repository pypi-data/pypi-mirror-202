import webbrowser
from sympy import *
import math


desmos_symbols = {chr(i): chr(i) for i in range(65, 91)}
desmos_symbols.update({chr(i): chr(i) for i in range(97, 123)})
desmos_symbols.update({
    'alpha': r'\alpha',
    'beta': r'\beta',
    'Delta': r'\Delta',
    'theta': r'\theta',
    'phi': r'\phi',
    'pi': r'\pi',
    'ln': r'\ln',
})


class Variable(Symbol):
    """extension of the sympy Symbol class to allow for quick and dirty interaction with the desmos graph"""
    def __new__(cls, symbol, graph):
        obj = Symbol.__new__(cls, symbol)
        obj.graph = graph
        return obj

    def __lt__(self, other):
        """appends the inequality to the graph"""
        self.graph.lt(self, other)

    def __le__(self, other):
        """appends the inequality to the graph"""
        self.graph.le(self, other)

    def __gt__(self, other):
        """appends the inequality to the graph"""
        self.graph.gt(self, other)

    def __ge__(self, other):
        """appends the inequality to the graph"""
        self.graph.ge(self, other)

    def __rshift__(self, other):
        """appends the equality to the graph"""
        self.graph.eq(self, other)

    def __call__(self, *args):
        """returns a symbolic representation of a function call"""
        return Variable(f'{self}({", ".join(to_latex(arg) for arg in args)})', self.graph)

    def __xor__(self, other):
        """appends an apostrophy to the symbol. useful for derivatives"""
        return Variable(str(self) + "'" * other, self.graph)

    def __getitem__(self, item):
        """appends a symbolic representation of a function call to the graph"""
        return self.graph(self(item))


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


class Graph:
    def __init__(self, graph_name='temp', api_key="dcb31709b452b1cf9dc26972add0fda6"):
        self.graph_name = graph_name
        self.file_name = graph_name + '.html'
        self.html = f'<body style="background-color:#2A2A2A;" marginwidth="0px" marginheight="0px">\n' \
                    f'<script src="https://www.desmos.com/api/v1.7/calculator.js?apiKey={api_key}"></script>\n' \
                    f'<div id="calculator"></div>\n' \
                    f'<script>\n' \
                    f'var elt = document.getElementById("calculator");\n' \
                    f'var calculator = Desmos.GraphingCalculator(elt);\n'
        self.expressions = 0
        for key, value in desmos_symbols.items():
            self.__setattr__(key, Variable(value, self))

    def new_expression(self, expression=None, **kwargs):
        """based on desmos api v1.7"""
        if isinstance(expression, dict):
            for key, value in expression.items():
                self.new_expression(f'{to_latex(key)} = {to_latex(value)}')
            expression = None
        if kwargs:
            for key, value in kwargs.items():
                self.new_expression(f'{key} = {to_latex(value)}')
        if expression is None:
            return
        expression = to_latex(expression)
        self.expressions += 1
        self.html += 'calculator.setExpression({ id: "graph%d", latex: %s });\n' % (self.expressions, repr(expression))

    def eq(self, lhs, rhs):
        """appends the equality to the graph"""
        self.new_expression(f'{to_latex(lhs)}={to_latex(rhs)}')

    def lt(self, lhs, rhs):
        """appends the inequality to the graph"""
        self.new_expression(f'{to_latex(lhs)}<{to_latex(rhs)}')

    def le(self, lhs, rhs):
        """appends the inequality to the graph"""
        self.new_expression(f'{to_latex(lhs)}\le {to_latex(rhs)}')

    def gt(self, lhs, rhs):
        """appends the inequality to the graph"""
        self.new_expression(f'{to_latex(lhs)}>{to_latex(rhs)}')

    def ge(self, lhs, rhs):
        """appends the inequality to the graph"""
        self.new_expression(f'{to_latex(lhs)}\ge {to_latex(rhs)}')

    def new_slider(self, key, value, min=-10, max=10, step='""'):
        """based on desmos api v1.7"""
        expression = f'{to_latex(key)} = {to_latex(value)}'
        self.expressions += 1
        self.html += 'calculator.setExpression({ id: "graph%d", latex: %s, sliderBounds: { min: %s, max: %s, step: %s } });\n' % (self.expressions, repr(to_latex(expression)), str(min), str(max), str(step))

    def new_table(self, values):
        """based on desmos api v1.7"""
        self.html += 'calculator.setExpression({ type: "table", columns: ['
        self.html += ', '.join('{latex: %s, values: %s}' % (repr(key), repr([to_latex(v) for v in value]))
                               for key, value in values.items())
        self.html += ']});'

    def save(self):
        print(self.html)
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
        """convenient wrapper for the new_expression, new_slider, and new_table methods"""
        slider_kwargs = ('min', 'max', 'step')
        if any(key in kwargs for key in slider_kwargs):
            for key, value in kwargs.items():
                if key not in slider_kwargs:
                    break
            self.new_slider(key, value, **{key: value for key, value in kwargs.items() if key in slider_kwargs})
            return
        if any(isinstance(value, list) for value in kwargs.values()):
            self.new_table({to_latex(key): value for key, value in kwargs.items()})
            return
        self.new_expression(*args, **kwargs)

    def plot_function(self, function, min, max, step=1):
        """wrapper of the self.new_table method"""
        N = math.ceil((max - min) / step)
        X = [min + step * n for n in range(int(N))]
        Y = [function(x) for x in X]
        self.new_table({'x': X, 'y': Y})

    def __or__(self, other):
        """wrapper of the __call__ method"""
        self.__call__(other)
