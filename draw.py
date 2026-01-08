"""
Function visualization module for AnCalc
Uses matplotlib for plotting mathematical functions
"""

import matplotlib.pyplot as plt
import numpy as np
from symbolic_math import symbols
from solver import evaluate_expr


def plot_function(expression, var_name='x', x_min=-10, x_max=10, points=500, title=None, export_path=None):
    """
    Plot a mathematical function over a specified range
    
    Args:
        expression: Symbolic expression or string to plot
        var_name: Variable name (default 'x')
        x_min: Minimum x value (default -10)
        x_max: Maximum x value (default 10)
        points: Number of points to plot (default 500)
        title: Plot title (optional)
        export_path: Path to save the plot (optional, e.g., 'plot.png')
    
    Returns:
        None (displays the plot)
    """
    # Create x values
    x_values = np.linspace(x_min, x_max, points)
    y_values = []
    
    # Get the variable symbol
    var = symbols(var_name)
    
    # Evaluate the expression for each x value
    for x_val in x_values:
        try:
            y_val = evaluate_expr(expression, var, x_val)
            y_values.append(y_val)
        except:
            y_values.append(np.nan)  # Use NaN for undefined points
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, 'b-', linewidth=2)
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='k', linewidth=0.5)
    plt.axvline(x=0, color='k', linewidth=0.5)
    plt.xlabel(var_name, fontsize=12)
    plt.ylabel(f'f({var_name})', fontsize=12)
    
    if title:
        plt.title(title, fontsize=14)
    else:
        plt.title(f'Plot of f({var_name}) = {expression}', fontsize=14)
    
    # Export if path is provided
    if export_path:
        plt.savefig(export_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {export_path}")
    
    plt.show()


def plot_multiple(expressions, var_name='x', x_min=-10, x_max=10, points=500, labels=None, title=None, export_path=None):
    """
    Plot multiple mathematical functions on the same graph
    
    Args:
        expressions: List of symbolic expressions or strings
        var_name: Variable name (default 'x')
        x_min: Minimum x value (default -10)
        x_max: Maximum x value (default 10)
        points: Number of points to plot (default 500)
        labels: List of labels for each function (optional)
        title: Plot title (optional)
        export_path: Path to save the plot (optional)
    
    Returns:
        None (displays the plot)
    """
    x_values = np.linspace(x_min, x_max, points)
    var = symbols(var_name)
    
    plt.figure(figsize=(10, 6))
    
    colors = ['b', 'r', 'g', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    
    for i, expression in enumerate(expressions):
        y_values = []
        
        for x_val in x_values:
            try:
                y_val = evaluate_expr(expression, var, x_val)
                y_values.append(y_val)
            except:
                y_values.append(np.nan)
        
        color = colors[i % len(colors)]
        label = labels[i] if labels and i < len(labels) else f'f{i+1}({var_name})'
        plt.plot(x_values, y_values, color=color, linewidth=2, label=label)
    
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='k', linewidth=0.5)
    plt.axvline(x=0, color='k', linewidth=0.5)
    plt.xlabel(var_name, fontsize=12)
    plt.ylabel(f'f({var_name})', fontsize=12)
    plt.legend()
    
    if title:
        plt.title(title, fontsize=14)
    else:
        plt.title('Multiple Functions', fontsize=14)
    
    if export_path:
        plt.savefig(export_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {export_path}")
    
    plt.show()


def plot_derivative_comparison(expression, var_name='x', x_min=-10, x_max=10, points=500, export_path=None):
    """
    Plot a function alongside its derivative
    
    Args:
        expression: Symbolic expression
        var_name: Variable name (default 'x')
        x_min: Minimum x value (default -10)
        x_max: Maximum x value (default 10)
        points: Number of points to plot (default 500)
        export_path: Path to save the plot (optional)
    """
    from solver import derivative, simplify_derivative
    
    var = symbols(var_name)
    deriv_expr = simplify_derivative(derivative(expression, var))
    
    plot_multiple(
        [expression, deriv_expr],
        var_name=var_name,
        x_min=x_min,
        x_max=x_max,
        points=points,
        labels=[f'f({var_name})', f"f'({var_name})"],
        title=f"Function and its Derivative",
        export_path=export_path
    )


# TODO: Auto adapt the function's range, allow user to move around graph etc
# TODO: Add interactive zooming and panning
# TODO: Add support for parametric plots
# TODO: Add 3D plotting capabilities
