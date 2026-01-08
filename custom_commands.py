def clear():
    """Clears the console screen."""
    import os
    import platform

    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def reload():
    """Reloads the program to apply changes."""
    import os
    import sys
    
    print("Reloading program...")
    os.execv(sys.executable, ['python'] + sys.argv)


def quit():
    """Quits the program"""
    exit()
