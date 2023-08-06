PyDesmos is a simple compiler of HTML based on the [Desmos API](https://www.desmos.com/api/v1.7/docs/index.html#document-layout).

The Graph class can automatically convert any latex-friendly [sympy](https://www.sympy.org/en/index.html) into HTML. That HTML can be then be saved and opened as a local Desmos graph.
It can also do much more, as seen in the following example. Try it yourself!

```python
from PyDesmos import Graph
import sympy as sp

with Graph('my_graph') as G:
    x, y, f, alpha, r, theta = G.x, G.y, G.f, G.alpha, G.r, G.theta
    G | x ** 2  # appends the expression "x ** 2" to the desmos graph
    f(x) >> sp.factorial(x - 1)  # appends the expression "f(x) = (x-1)!"
    G(alpha=2, min=0, max=1, step=0.5)  # appends a slider "a" with respective bounds
    G(x=[0, 1, 2], y=[alpha, 2 * alpha, 3 * alpha])  # appends a table
    G.plot_function(lambda x: 1/x, min=1, max=100, step=2)  # appends a table plotting the function "1/x" from 1 to 100 with step-size 2
    r < 1 + sp.sin(theta)  # appends the inequality "y < 1 + sin(θ)"
    G(p=(1, 1))  # appends the point "p=(1, 1)"

# opens my_graph.html when the with-statement exits
```