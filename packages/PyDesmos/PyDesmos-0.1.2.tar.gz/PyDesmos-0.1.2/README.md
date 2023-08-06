We'll keep it simple. [Desmos](https://www.desmos.com/calculator) is one of the best online calculators.
Python is one of the best programming languages. So why no Python API? Who knows.
What we do know is that PyDesmos is the next best thing.

We've made it as easy as possible to interact with Desmos from python:
```python
from PyDesmos import Graph
with Graph('my graph') as G:
    f, x = G.f, G.x
    f[x] = x ** 2
```
With just these four lines: _an HTML file called "my graph.html" containing a Desmos graph with the expression "f(x)=x^2" already written, is compiled and then automatically opened in your favorite browser!_

Magic? Yes. But that's not all. We've pushed Python's syntax to its limits to make your experience as simple as possible.
Our flexible code incidentally allows many alternatives to `f[x] = x ** 2`, depending on your style / needs:

```python
G.append('f(x)=x^2')
G.define('f(x)', x ** 2)  # 'f(x)' is also equivalent to f(x) (yes, without quotes)
G.eq(f(x), x ** 2)
G(f(x), '=', x ** 2)
G(f(x), x ** 2)
G[f(x)] = x ** 2
```

Many more things are made easy. For example, plotting tables:

```python
G.new_table({x: [0, 1, 2], y: [2, 3, 5]})  # where x, y = G.x, G.y, OR
G(x=[0, 1, 2], y=[2, 3, 5])
```

Plotting python functions:
```python
f = lambda x: int(str(x)[::-1])
G.plot_function(f, 0, 100)  # OR
G(f, min=0, max=100)
```

Since Desmos uses latex to generate expressions, all latex-friendly [sympy](https://www.sympy.org/en/index.html) expressions get automatically converted.
```python
import sympy as sp
with Graph('my graph') as G:
    x, y = G.x, G.y
    G.le(sp.factorial(x + y), sp.sin(x - y))  # appends the expression "(x+y)! <= sin(x-y)"
```
Sliders and greek letter support:
```python
G(alpha=0, min=0, max=2 * G.pi, step=G.pi / 2)  # appends the constant "α=0" with respective bounds
```
Yet another way to append expressions:
```python
G | sympy.sin(2 * G.x)  # appends the expression "sin(2x)"
```
Points:
```python
G(p=(0,0))  # appends the point "p=(0,0)"
```
Prime-notation:
```python
G | (f^1)(x)  # appends the expression "f'(x)", where f, x = G.f, x.f
```
Subscript notation:
```python
G(c[0], 42)  # appends the expression "c_{0}=42", where c = G.c
```
...

Alright, I'm sure you get it. PyDesmos is awesome. But one last thing. All of these methods have additional (optional) kwargs for absolute customization, such as color, line thickness, etc.
You may read about them [here](https://www.desmos.com/api/v1.7/docs/index.html#document-manipulating-expressions), under "expression_state Name and Values". For example,
```python
G(y=G.x ** 2, color='#FF0000')  # appends the expression "y=x^2" with color #FF0000.
```
Happy PyDesmos-ing!

---

**New:** To plot a sequence from the [OEIS](https://oeis.org/):
```python
G.plot_oeis('A000001')  # optional max_terms parameter
```
Or to just get a dictionary:
```python
A000001 = oeis('A000001')  # {0: 0, 1: 1, ...}
```