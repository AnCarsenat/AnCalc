from symbolic_math import Pow, Add, Sub, Mul, Div, Symbol, Eq


def simplify_expr(expr, var):
    """Recursively simplify expression by evaluating constants"""
    if isinstance(expr, (int, float)):
        return expr
    
    if isinstance(expr, Symbol):
        return expr
    
    if isinstance(expr, Add):
        left = simplify_expr(expr.left, var)
        right = simplify_expr(expr.right, var)
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left + right
        return Add(left, right)
    
    if isinstance(expr, Sub):
        left = simplify_expr(expr.left, var)
        right = simplify_expr(expr.right, var)
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left - right
        return Sub(left, right)
    
    if isinstance(expr, Mul):
        left = simplify_expr(expr.left, var)
        right = simplify_expr(expr.right, var)
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left * right
        return Mul(left, right)
    
    if isinstance(expr, Div):
        left = simplify_expr(expr.left, var)
        right = simplify_expr(expr.right, var)
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left / right
        return Div(left, right)
    
    if isinstance(expr, Pow):
        base = simplify_expr(expr.base, var)
        exp = simplify_expr(expr.exp, var)
        if isinstance(base, (int, float)) and isinstance(exp, (int, float)):
            return base ** exp
        return Pow(base, exp)
    
    return expr


def evaluate_expr(expr, var, value):
    """Evaluate expression by substituting var with value"""
    if isinstance(expr, (int, float)):
        return expr
    
    if isinstance(expr, Symbol):
        if expr.name == var.name:
            return value
        return expr
    
    if isinstance(expr, Add):
        return evaluate_expr(expr.left, var, value) + evaluate_expr(expr.right, var, value)
    
    if isinstance(expr, Sub):
        return evaluate_expr(expr.left, var, value) - evaluate_expr(expr.right, var, value)
    
    if isinstance(expr, Mul):
        return evaluate_expr(expr.left, var, value) * evaluate_expr(expr.right, var, value)
    
    if isinstance(expr, Div):
        return evaluate_expr(expr.left, var, value) / evaluate_expr(expr.right, var, value)
    
    if isinstance(expr, Pow):
        return evaluate_expr(expr.base, var, value) ** evaluate_expr(expr.exp, var, value)
    
    return expr


def solve_linear(eq, var):
    """Solve linear equation: ax + b = 0"""
    # Move everything to left side
    left = simplify_expr(Sub(eq.left, eq.right), var)
    
    # Extract coefficient and constant
    a = 0  # coefficient of var
    b = 0  # constant term
    
    def extract_terms(expr):
        nonlocal a, b
        
        if isinstance(expr, (int, float)):
            b += expr
        elif isinstance(expr, Symbol):
            if expr.name == var.name:
                a += 1
        elif isinstance(expr, Add):
            extract_terms(expr.left)
            extract_terms(expr.right)
        elif isinstance(expr, Sub):
            extract_terms(expr.left)
            # Subtract right side
            orig_a, orig_b = a, b
            a, b = 0, 0
            extract_terms(expr.right)
            right_a, right_b = a, b
            a, b = orig_a - right_a, orig_b - right_b
        elif isinstance(expr, Mul):
            # Check if one side is constant and other is var
            if isinstance(expr.left, (int, float)) and isinstance(expr.right, Symbol):
                if expr.right.name == var.name:
                    a += expr.left
            elif isinstance(expr.right, (int, float)) and isinstance(expr.left, Symbol):
                if expr.left.name == var.name:
                    a += expr.right
            else:
                # Try to evaluate
                try:
                    val = evaluate_expr(expr, var, 0)
                    if isinstance(val, (int, float)):
                        b += val
                except:
                    pass
    
    extract_terms(left)
    
    # Solve ax + b = 0 => x = -b/a
    if a != 0:
        return [-b / a]
    else:
        return []


def solve_quadratic(eq, var):
    """Solve quadratic equation: ax^2 + bx + c = 0"""
    # Move everything to left side
    left = simplify_expr(Sub(eq.left, eq.right), var)
    
    # Extract coefficients
    a = 0  # coefficient of x^2
    b = 0  # coefficient of x
    c = 0  # constant
    
    def extract_quadratic_terms(expr):
        nonlocal a, b, c
        
        if isinstance(expr, (int, float)):
            c += expr
        elif isinstance(expr, Symbol):
            if expr.name == var.name:
                b += 1
        elif isinstance(expr, Add):
            extract_quadratic_terms(expr.left)
            extract_quadratic_terms(expr.right)
        elif isinstance(expr, Sub):
            extract_quadratic_terms(expr.left)
            orig_a, orig_b, orig_c = a, b, c
            a, b, c = 0, 0, 0
            extract_quadratic_terms(expr.right)
            right_a, right_b, right_c = a, b, c
            a, b, c = orig_a - right_a, orig_b - right_b, orig_c - right_c
        elif isinstance(expr, Mul):
            if isinstance(expr.left, (int, float)) and isinstance(expr.right, Symbol):
                if expr.right.name == var.name:
                    b += expr.left
            elif isinstance(expr.right, (int, float)) and isinstance(expr.left, Symbol):
                if expr.left.name == var.name:
                    b += expr.right
            elif isinstance(expr.left, (int, float)) and isinstance(expr.right, Pow):
                if isinstance(expr.right.base, Symbol) and expr.right.base.name == var.name:
                    if isinstance(expr.right.exp, (int, float)) and expr.right.exp == 2:
                        a += expr.left
            elif isinstance(expr.right, (int, float)) and isinstance(expr.left, Pow):
                if isinstance(expr.left.base, Symbol) and expr.left.base.name == var.name:
                    if isinstance(expr.left.exp, (int, float)) and expr.left.exp == 2:
                        a += expr.right
        elif isinstance(expr, Pow):
            if isinstance(expr.base, Symbol) and expr.base.name == var.name:
                if isinstance(expr.exp, (int, float)) and expr.exp == 2:
                    a += 1
    
    extract_quadratic_terms(left)
    
    # Solve using quadratic formula: x = (-b ± sqrt(b^2 - 4ac)) / 2a
    if a != 0:
        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            return []  # No real solutions
        elif discriminant == 0:
            return [-b / (2*a)]
        else:
            sqrt_disc = discriminant ** 0.5
            sol1 = (-b + sqrt_disc) / (2*a)
            sol2 = (-b - sqrt_disc) / (2*a)
            return sorted([sol1, sol2])
    else:
        # Not quadratic, try linear
        return solve_linear(eq, var)


def solve(eq, var):
    """
    Solve equation for given variable
    
    Args:
        eq: Equation object (Eq)
        var: Symbol to solve for
    
    Returns:
        list: List of solutions
    """
    # Determine equation type
    # First try quadratic
    solutions = solve_quadratic(eq, var)
    if solutions:
        return solutions
    
    # Try linear
    solutions = solve_linear(eq, var)
    return solutions


def derivative(expr, var):
    """
    Compute the derivative of an expression with respect to a variable
    
    Args:
        expr: Expression to differentiate
        var: Symbol to differentiate with respect to
    
    Returns:
        Expression: The derivative
    """
    # Constant rule: d/dx(c) = 0
    if isinstance(expr, (int, float)):
        return 0
    
    # Variable rule: d/dx(x) = 1, d/dx(y) = 0
    if isinstance(expr, Symbol):
        if expr.name == var.name:
            return 1
        else:
            return 0
    
    # Sum rule: d/dx(f + g) = f' + g'
    if isinstance(expr, Add):
        left_deriv = derivative(expr.left, var)
        right_deriv = derivative(expr.right, var)
        return Add(left_deriv, right_deriv)
    
    # Difference rule: d/dx(f - g) = f' - g'
    if isinstance(expr, Sub):
        left_deriv = derivative(expr.left, var)
        right_deriv = derivative(expr.right, var)
        return Sub(left_deriv, right_deriv)
    
    # Product rule: d/dx(f * g) = f' * g + f * g'
    if isinstance(expr, Mul):
        f = expr.left
        g = expr.right
        f_prime = derivative(f, var)
        g_prime = derivative(g, var)
        return Add(Mul(f_prime, g), Mul(f, g_prime))
    
    # Quotient rule: d/dx(f / g) = (f' * g - f * g') / g^2
    if isinstance(expr, Div):
        f = expr.left
        g = expr.right
        f_prime = derivative(f, var)
        g_prime = derivative(g, var)
        numerator = Sub(Mul(f_prime, g), Mul(f, g_prime))
        denominator = Pow(g, 2)
        return Div(numerator, denominator)
    
    # Power rule: d/dx(x^n) = n * x^(n-1)
    if isinstance(expr, Pow):
        base = expr.base
        exponent = expr.exp
        
        # Special case: d/dx(x^n) where n is constant
        if isinstance(base, Symbol) and base.name == var.name:
            if isinstance(exponent, (int, float)):
                # n * x^(n-1)
                new_exp = exponent - 1
                coeff = exponent
                if new_exp == 0:
                    return coeff
                elif new_exp == 1:
                    return Mul(coeff, base)
                else:
                    return Mul(coeff, Pow(base, new_exp))
        
        # General case: d/dx(f^g) = f^g * (g' * ln(f) + g * f'/f)
        # For simplicity, handle constant exponent case
        if isinstance(exponent, (int, float)):
            # Chain rule: n * f^(n-1) * f'
            base_deriv = derivative(base, var)
            return Mul(Mul(exponent, Pow(base, exponent - 1)), base_deriv)
        
        # If both are variables/expressions, it's more complex
        # Return a simplified form or raise error
        return 0
    
    return 0


def simplify_derivative(expr):
    """Simplify a derivative expression"""
    if isinstance(expr, (int, float)):
        return expr
    
    if isinstance(expr, Symbol):
        return expr
    
    if isinstance(expr, Add):
        left = simplify_derivative(expr.left)
        right = simplify_derivative(expr.right)
        
        # 0 + x = x
        if isinstance(left, (int, float)) and left == 0:
            return right
        if isinstance(right, (int, float)) and right == 0:
            return left
        
        # Combine constants
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left + right
        
        return Add(left, right)
    
    if isinstance(expr, Sub):
        left = simplify_derivative(expr.left)
        right = simplify_derivative(expr.right)
        
        # x - 0 = x
        if isinstance(right, (int, float)) and right == 0:
            return left
        # 0 - x = -x
        if isinstance(left, (int, float)) and left == 0:
            return Mul(-1, right)
        
        # Combine constants
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left - right
        
        return Sub(left, right)
    
    if isinstance(expr, Mul):
        left = simplify_derivative(expr.left)
        right = simplify_derivative(expr.right)
        
        # 0 * x = 0
        if (isinstance(left, (int, float)) and left == 0) or (isinstance(right, (int, float)) and right == 0):
            return 0
        # 1 * x = x
        if isinstance(left, (int, float)) and left == 1:
            return right
        if isinstance(right, (int, float)) and right == 1:
            return left
        
        # Combine constants
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left * right
        
        return Mul(left, right)
    
    if isinstance(expr, Div):
        left = simplify_derivative(expr.left)
        right = simplify_derivative(expr.right)
        
        # 0 / x = 0
        if isinstance(left, (int, float)) and left == 0:
            return 0
        # x / 1 = x
        if isinstance(right, (int, float)) and right == 1:
            return left
        
        # Combine constants
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left / right
        
        return Div(left, right)
    
    if isinstance(expr, Pow):
        base = simplify_derivative(expr.base)
        exp = simplify_derivative(expr.exp)
        
        # x^0 = 1
        if isinstance(exp, (int, float)) and exp == 0:
            return 1
        # x^1 = x
        if isinstance(exp, (int, float)) and exp == 1:
            return base
        # 0^n = 0 (for n > 0)
        if isinstance(base, (int, float)) and base == 0:
            return 0
        # 1^n = 1
        if isinstance(base, (int, float)) and base == 1:
            return 1
        
        # Combine constants
        if isinstance(base, (int, float)) and isinstance(exp, (int, float)):
            return base ** exp
        
        return Pow(base, exp)
    
    return expr