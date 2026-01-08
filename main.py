import globals

from symbolic_math import symbols, Eq
from solver import solve, derivative, simplify_derivative
from utils import format_solution
from draw import plot_function
import re

import custom_commands


def process_command(command: str) -> tuple or str:
    """
    Processes a single command string and evaluates it.

    Args : 
        - command (str): The command string to evaluate

    Returns :
        - result: The result of the evaluation

    NOTE If process_command fails returns error with error str (Error:str)
    """
    try:
        command = command.strip()
        if not command:
            return None
        
        # Check if it's a derivative command
        if command.startswith("derivative ") or command.startswith("deriv ") or command.startswith("d/d"):
            # Check for help first
            if "help" in command.lower():
                return """
Derivative Command:
  Computes the derivative of a function with respect to a variable.
  
  Formats:
    - deriv <expression> <variable>
    - derivative <expression> <variable>
    - d/d<variable> <expression>
  
  Examples:
    - deriv x**2 x
    - derivative x**3 + 2*x x
    - d/dx x**2
    - d/dx (x + 1)**2
"""

            # Handle formats like: "derivative x**2 x" or "d/dx x**2"
            if command.startswith("d/d"):
                # Format: d/dx expression
                match = re.match(r'd/d([a-z])\s+(.+)', command)
                if not match:
                    return "Error: Format should be 'd/dx expression'"
                var_name = match.group(1)
                expr_str = match.group(2).strip()
            else:
                # Format: derivative/deriv expression variable
                parts = command.split()
                if len(parts) < 3:
                    return "Error: Format should be 'derivative expression variable' or 'd/dx expression'"
                var_name = parts[-1]  # Last part is the variable
                expr_str = ' '.join(parts[1:-1])  # Middle parts are the expression
            
            var = symbols(var_name)
            
            # Create namespace for eval with the variable
            namespace = {var_name: var}
            
            # Evaluate expression
            expr = eval(expr_str, {"__builtins__": {}}, namespace)
            
            # Compute derivative
            deriv = derivative(expr, var)
            simplified = simplify_derivative(deriv)
            
            return f"d/d{var_name}({expr_str}) = {simplified}"
        
        # Check if it's a solve command
        if command.startswith("solve "):
            # Extract equation after "solve "
            eq_str = command[6:].strip()

            if "help" in eq_str.lower():
                return """
Solve Command:
  Solves algebraic equations (linear and quadratic).
  
  Format:
    - solve <equation>
  
  Examples:
    - solve x**2 - 4 = 0
    - solve x**2 + 5*x + 6 = 0
    - solve 2*x + 4 = 0
"""
            
            # Parse the equation - expecting format like "x**2 - 4 = 0"
            if "=" not in eq_str:
                return "Error: Equation must contain '='"
            
            # Extract variable (look for single letter variables)
            var_matches = re.findall(r'\b([a-z])\b', eq_str)
            if not var_matches:
                return "Error: No variable found in equation"
            
            var_name = var_matches[0]  # Use first variable found
            var = symbols(var_name)
            
            # Split by = to get left and right sides
            parts = eq_str.split("=")
            if len(parts) != 2:
                return "Error: Equation must have exactly one '='"
            
            left_str = parts[0].strip()
            right_str = parts[1].strip()
            
            # Create namespace for eval with the variable
            namespace = {var_name: var}
            
            # Evaluate both sides
            left_expr = eval(left_str, {"__builtins__": {}}, namespace)
            right_expr = eval(right_str, {"__builtins__": {}}, namespace)
            
            # Create equation
            equation = Eq(left_expr, right_expr)
            
            # Solve
            solutions = solve(equation, var)
            
            if not solutions:
                return "No solutions found"
            elif len(solutions) == 1:
                return f"{var_name} = {solutions[0]}"
            else:
                sol_str = ", ".join([str(s) for s in solutions])
                return f"{var_name} = [{sol_str}]"

        # Check if it's a draw command
        if command.startswith("draw "):
            # Extract expression after "draw "
            expr_str = command[5:].strip()

            if "help" in expr_str.lower():
                return """
Draw Command:
  Plots a mathematical function using matplotlib.
  
  Formats:
    - draw <expression>
    - draw <expression> <x_min> <x_max>
  
  Examples:
    - draw x**2
    - draw x**3 - 3*x
    - draw x**2 -5 5
    - draw x**3 + 2*x**2 -3 3
"""
            
            # Parse format: "draw x**2" or "draw x**2 -5 5" or "draw x**2 x -5 5"
            parts = expr_str.split()
            
            # Extract variable (look for single letter variables in the expression)
            var_matches = re.findall(r'\b([a-z])\b', parts[0])
            if not var_matches:
                return "Error: No variable found in expression"
            
            var_name = var_matches[0]  # Use first variable found
            var = symbols(var_name)
            
            # Default range
            x_min, x_max = -10, 10
            
            # Check if range is provided
            if len(parts) >= 3:
                # Last two parts might be the range
                try:
                    x_min = float(parts[-2])
                    x_max = float(parts[-1])
                    # Remove range from expression
                    expr_str = ' '.join(parts[:-2])
                except ValueError:
                    # Not a range, use full expression
                    expr_str = ' '.join(parts)
            else:
                expr_str = ' '.join(parts)
            
            # Create namespace for eval with the variable
            namespace = {var_name: var}
            
            # Evaluate expression
            try:
                expr = eval(expr_str, {"__builtins__": {}}, namespace)
                
                # Plot the function
                plot_function(
                    expr,
                    var_name=var_name,
                    x_min=x_min,
                    x_max=x_max,
                    title=f"f({var_name}) = {expr_str}"
                )
                
                return f"Plotting f({var_name}) = {expr_str} from {x_min} to {x_max}"
            except Exception as e:
                return f"Error plotting: {e}"
        
        # Process regular exec command
        if command.startswith("!") and globals.ALLOW_RUN_COMMANDS:
            exec(command[1:])
            return "Executed"

        # Process custom commands
        if command.startswith(":"):
            try:
                command_name = command[1:]  # Remove the ":"
                result = getattr(custom_commands, command_name)()
                return result if result is not None else "Command executed"
            except Exception as errorMessage:
                return f"Error: {errorMessage}"
        
        # Display help message if needed
        if command.startswith("help"):
            return """
AnCalc - Advanced Calculator
==============================

Available Commands:

1. Basic Math:
   - Enter any mathematical expression
   - Examples: 5*5, 2+3, 10/2, 2**3

2. solve <equation>
   - Solves linear and quadratic equations
   - Example: solve x**2 - 4 = 0
   - Type 'solve help' for more info

3. derivative/deriv/d/d<var> <expression>
   - Computes derivatives
   - Examples: deriv x**2 x, d/dx x**2
   - Type 'deriv help' for more info

4. draw <expression> [x_min] [x_max]
   - Plots functions
   - Examples: draw x**2, draw x**3 -5 5
   - Type 'draw help' for more info

5. Custom Commands (prefix with :)
   - :clear - Clear the screen
   - :reload - Reload the program

6. Execute Python (prefix with !)
   - !print("Hello") - Run Python code
   - Requires ALLOW_RUN_COMMANDS = True

7. Multiple Commands:
   - Use & for sequential: 5*5 & 3+2
   - Use | for async: solve x**2-4=0 | draw x**2

For detailed help on a command, type: <command> help
"""


        # Regular eval
        result = eval(command)
        return result
        
    except Exception as e:
        return f"Error: {e}"



while True:
    userInput: str = input("> ")  # Get input from user
    results = []
    
    if not userInput.strip():
        continue

    # Convert userInput to usable commands
    # Split by " | " for async commands
    async_groups = userInput.split(" | ")
    for async_group in async_groups:
        # Split by " & " for stacked commands within each group
        commands = async_group.split(" & ")
        for command in commands:
            result = process_command(command)
            if result is not None:
                results.append(result)
    
    # Output results
    for result in results:
        print(result)