from functools import wraps


def day_started_required(func):
    """
    A decorator that checks if the 'current_day' attribute of an object is set before executing a method.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.

    Raises:
        None

    Example Usage:
        @day_started_required
        def perform_task(self):
            # code to perform the task
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.current_day:
            return "Você não iniciou o dia. Portanto não é possível realizar esta operação"
        return func(self, *args, **kwargs)
    return wrapper


def are_there_packges_in_the_truck(func):
    """
    A decorator that checks if there are packages in the truck before executing the decorated function.

    Args:
        func: The function to be decorated.

    Returns:
        If there are no packages in the truck, returns the string "Não há pacotes no caminhão".
        If there are packages in the truck, calls the original `func` with the given arguments and returns the result.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if len(self.load_list) == 0:
            return "Não há pacotes no caminhão"
        return func(self, *args, **kwargs)
    return wrapper
