"""
Custom symbolic math system
Supports basic symbolic operations and expressions
"""

class Symbol:
    """Represents a symbolic variable"""
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name
    
    def __add__(self, other):
        return Add(self, other)
    
    def __sub__(self, other):
        return Sub(self, other)
    
    def __mul__(self, other):
        return Mul(self, other)
    
    def __truediv__(self, other):
        return Div(self, other)
    
    def __pow__(self, other):
        return Pow(self, other)
    
    def __radd__(self, other):
        return Add(other, self)
    
    def __rsub__(self, other):
        return Sub(other, self)
    
    def __rmul__(self, other):
        return Mul(other, self)
    
    def __rtruediv__(self, other):
        return Div(other, self)
    
    def __rpow__(self, other):
        return Pow(other, self)
    
    def __neg__(self):
        return Mul(-1, self)
    
    def __eq__(self, other):
        return Eq(self, other)


class Expr:
    """Base class for expressions"""
    pass


class Add(Expr):
    """Addition expression"""
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"({self.left} + {self.right})"
    
    def __add__(self, other):
        return Add(self, other)
    
    def __sub__(self, other):
        return Sub(self, other)
    
    def __mul__(self, other):
        return Mul(self, other)
    
    def __truediv__(self, other):
        return Div(self, other)
    
    def __pow__(self, other):
        return Pow(self, other)
    
    def __eq__(self, other):
        return Eq(self, other)


class Sub(Expr):
    """Subtraction expression"""
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"({self.left} - {self.right})"
    
    def __add__(self, other):
        return Add(self, other)
    
    def __sub__(self, other):
        return Sub(self, other)
    
    def __mul__(self, other):
        return Mul(self, other)
    
    def __truediv__(self, other):
        return Div(self, other)
    
    def __pow__(self, other):
        return Pow(self, other)
    
    def __eq__(self, other):
        return Eq(self, other)


class Mul(Expr):
    """Multiplication expression"""
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"({self.left} * {self.right})"
    
    def __add__(self, other):
        return Add(self, other)
    
    def __sub__(self, other):
        return Sub(self, other)
    
    def __mul__(self, other):
        return Mul(self, other)
    
    def __truediv__(self, other):
        return Div(self, other)
    
    def __pow__(self, other):
        return Pow(self, other)
    
    def __eq__(self, other):
        return Eq(self, other)


class Div(Expr):
    """Division expression"""
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"({self.left} / {self.right})"
    
    def __add__(self, other):
        return Add(self, other)
    
    def __sub__(self, other):
        return Sub(self, other)
    
    def __mul__(self, other):
        return Mul(self, other)
    
    def __truediv__(self, other):
        return Div(self, other)
    
    def __pow__(self, other):
        return Pow(self, other)
    
    def __eq__(self, other):
        return Eq(self, other)


class Pow(Expr):
    """Power expression"""
    def __init__(self, base, exp):
        self.base = base
        self.exp = exp
    
    def __repr__(self):
        return f"({self.base}**{self.exp})"
    
    def __add__(self, other):
        return Add(self, other)
    
    def __sub__(self, other):
        return Sub(self, other)
    
    def __mul__(self, other):
        return Mul(self, other)
    
    def __truediv__(self, other):
        return Div(self, other)
    
    def __pow__(self, other):
        return Pow(self, other)
    
    def __eq__(self, other):
        return Eq(self, other)


class Eq:
    """Equation class"""
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"{self.left} = {self.right}"


def symbols(names):
    """Create symbolic variables"""
    if isinstance(names, str):
        if ',' in names:
            names = [n.strip() for n in names.split(',')]
            return tuple(Symbol(n) for n in names)
        else:
            return Symbol(names)
    return tuple(Symbol(n) for n in names)
