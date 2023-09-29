
from core.core import RunProgram
from core.truck import Truck
from menu.menu import Menu

def main():
    """
    The `main` function is the entry point of the program. It displays a menu to the user and executes different processes based on the user's choice.

    Example Usage:
    main()

    Inputs:
    - None

    Flow:
    1. Create an instance of the `Truck` class.
    2. Enter a while loop that continues until the user chooses to exit.
    3. Display the main menu to the user.
    4. Get the user's choice.
    5. Create an instance of the `RunProgram` class with the `Truck` instance as a parameter.
    6. Call the `run` method of the `RunProgram` instance with the user's choice as a parameter.
    7. Repeat steps 3-6 until the user chooses to exit.

    Outputs:
    - Truck Manager execution
    """

    main_menu_list = [
        "Bem-Vindo ao Truck Manager!",
        "1. Iniciar dia",
        "2. Realizar parada",
        "3. Consultar situação",
        "4. Listar pacotes",
        "5. Finalizar dia",
        "6. Gerar relatório",
        "7. Sair"
    ]

    truck = Truck()

    while True:
        main_menu = Menu(main_menu_list)
        opt = main_menu.run()
        program = RunProgram(truck)
        program.run(opt)



if __name__ == "__main__":
    main()