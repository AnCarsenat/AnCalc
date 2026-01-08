"""
Test script for the custom symbolic math and solver system
"""

# Import from our custom modules
from symbolic_math import symbols, Eq
from solver import solve

# Test 1: Simple quadratic equation x^2 - 4 = 0
print("Test 1: x^2 - 4 = 0")
x = symbols('x')
eq = Eq(x**2 - 4, 0)
print(f"Equation: {eq}")
solutions = solve(eq, x)
print(f"Solutions: {solutions}")
print()

# Test 2: Another quadratic x^2 + 5x + 6 = 0
print("Test 2: x^2 + 5x + 6 = 0")
eq2 = Eq(x**2 + 5*x + 6, 0)
print(f"Equation: {eq2}")
solutions2 = solve(eq2, x)
print(f"Solutions: {solutions2}")
print()

# Test 3: Linear equation 2x + 4 = 0
print("Test 3: 2x + 4 = 0")
eq3 = Eq(2*x + 4, 0)
print(f"Equation: {eq3}")
solutions3 = solve(eq3, x)
print(f"Solutions: {solutions3}")
print()

# Test 4: Perfect square (x - 3)^2 = 0
print("Test 4: x^2 - 6x + 9 = 0")
eq4 = Eq(x**2 - 6*x + 9, 0)
print(f"Equation: {eq4}")
solutions4 = solve(eq4, x)
print(f"Solutions: {solutions4}")
