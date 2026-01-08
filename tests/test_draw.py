"""
Test script for the draw module
"""

from symbolic_math import symbols
from draw import plot_function, plot_multiple, plot_derivative_comparison

# Get the variable
x = symbols('x')

# Test 1: Plot a simple quadratic function
print("Test 1: Plotting x^2")
plot_function(x**2, var_name='x', x_min=-5, x_max=5, title="Quadratic Function")

# Test 2: Plot a cubic function
print("Test 2: Plotting x^3 - 3x")
plot_function(x**3 - 3*x, var_name='x', x_min=-3, x_max=3, title="Cubic Function")

# Test 3: Plot multiple functions
print("Test 3: Plotting multiple functions")
plot_multiple(
    [x**2, x**3, 2*x],
    var_name='x',
    x_min=-3,
    x_max=3,
    labels=['x²', 'x³', '2x'],
    title="Multiple Functions"
)

# Test 4: Plot function with its derivative
print("Test 4: Plotting function with derivative")
plot_derivative_comparison(x**3 - 3*x, var_name='x', x_min=-3, x_max=3)

# Test 5: Export a plot
print("Test 5: Exporting plot to file")
plot_function(
    x**2 + 2*x + 1,
    var_name='x',
    x_min=-5,
    x_max=5,
    title="Exported Function",
    export_path="test_plot.png"
)

print("\nAll tests completed!")
