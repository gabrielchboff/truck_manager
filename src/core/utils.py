from os import system, name


def clear():
    """
    Clears the terminal screen.

    This function checks the operating system and uses the appropriate command (`cls` for Windows and `clear` for Unix-based systems) to clear the screen.

    Example Usage:
    ```python
    clear()
    ```

    Inputs:
    There are no inputs for the `clear` function.

    Flow:
    1. The function checks the value of the `name` variable, which stores the name of the operating system.
    2. If the `name` is equal to `'nt'`, indicating a Windows operating system, the function calls the `system` function with the command `'cls'` to clear the screen.
    3. If the `name` is not equal to `'nt'`, indicating a Unix-based operating system, the function calls the `system` function with the command `'clear'` to clear the screen.

    Outputs:
    The `clear` function does not return any output.
    """
    return system('cls') if name == 'nt' else system('clear')
