def format_solution(solutions):
    """Format solutions for display"""
    if not solutions:
        return "No solutions found"
    
    if len(solutions) == 1:
        return f"x = {solutions[0]}"
    
    formatted = ", ".join([str(s) for s in solutions])
    return f"x = [{formatted}]"


def is_number(s):
    """Check if string represents a number"""
    try:
        float(s)
        return True
    except ValueError:
        return False
