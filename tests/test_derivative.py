"""
Test script for the derivative function
"""

from symbolic_math import symbols
from solver import derivative, simplify_derivative

# Create symbol
x = symbols('x')

# Test 1: Derivative of constant
print("Test 1: d/dx(5) = ?")
expr1 = 5
deriv1 = derivative(expr1, x)
simplified1 = simplify_derivative(deriv1)
print(f"Result: {simplified1}")
print()

# Test 2: Derivative of x
print("Test 2: d/dx(x) = ?")
deriv2 = derivative(x, x)
simplified2 = simplify_derivative(deriv2)
print(f"Result: {simplified2}")
print()

# Test 3: Derivative of x^2
print("Test 3: d/dx(x^2) = ?")
expr3 = x**2
print(f"Expression: {expr3}")
deriv3 = derivative(expr3, x)
print(f"Derivative (unsimplified): {deriv3}")
simplified3 = simplify_derivative(deriv3)
print(f"Result: {simplified3}")
print()

# Test 4: Derivative of 3x^2
print("Test 4: d/dx(3x^2) = ?")
expr4 = 3*x**2
deriv4 = derivative(expr4, x)
simplified4 = simplify_derivative(deriv4)
print(f"Result: {simplified4}")
print()

# Test 5: Derivative of x^3 + 2x^2 + x + 1
print("Test 5: d/dx(x^3 + 2x^2 + x + 1) = ?")
expr5 = x**3 + 2*x**2 + x + 1
deriv5 = derivative(expr5, x)
simplified5 = simplify_derivative(deriv5)
print(f"Result: {simplified5}")
print()

# Test 6: Derivative of x^2 * x^3 (product rule)
print("Test 6: d/dx(x^2 * x) = ?")
expr6 = x**2 * x
deriv6 = derivative(expr6, x)
simplified6 = simplify_derivative(deriv6)
print(f"Result: {simplified6}")
print()

# Test 7: Derivative of x^2 / x (quotient rule)
print("Test 7: d/dx(x^2 / x) = ?")
expr7 = x**2 / x
deriv7 = derivative(expr7, x)
simplified7 = simplify_derivative(deriv7)
print(f"Result: {simplified7}")
print()

# Test 8: Derivative of (x + 1)^2
print("Test 8: d/dx((x + 1)^2) = ?")
expr8 = (x + 1)**2
deriv8 = derivative(expr8, x)
simplified8 = simplify_derivative(deriv8)
print(f"Result: {simplified8}")
