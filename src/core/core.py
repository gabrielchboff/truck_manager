import sys
import time
from dataclasses import dataclass

from core.truck import Packge, Truck
from core.utils import clear
from menu.menu import Menu


"""
The `RunProgram` class is responsible for running the main program logic. It interacts with the user through a menu system and performs operations on the `Truck` object.

Example Usage:
    truck = Truck()
    program = RunProgram(truck)
    program.run(1)  # Start the day
    program.run(2)  # Perform stop operations
    program.run(3)  # Check the status of the truck
    program.run(4)  # List the packages in the truck
    program.run(5)  # End the day
    program.run(6)  # Generate a report
    program.run(7)  # Exit the program

Main functionalities:
- Start the day by setting the volume and weight of the truck's cargo.
- Perform stop operations, including inserting and removing packages.
- Check the status of the truck, including the current weight, remaining weight, and number of packages.
- List the packages in the truck.
- End the day and reset the truck's state.
- Generate a report with various statistics about the day's operations.
- Exit the program.

Methods:
- `animated_dots(duration, interval)`: Displays animated dots for a specified duration.
- `_start_day_process()`: Prompts the user for the volume and weight of the truck's cargo and starts the day.
- `_stop_process()`: Displays a menu for stop operations and performs the selected operation.
- `_check_status_process()`: Prints the current status of the truck.
- `_list_packages_process()`: Prints the list of packages in the truck.
- `_end_day_process()`: Ends the day and resets the truck's state.
- `_generate_report_process()`: Generates a report with various statistics about the day's operations.
- `run(choice)`: Executes the corresponding process based on the user's choice.

Fields:
- `current_truck`: The `Truck` object representing the truck being operated on.
"""


@dataclass
class RunProgram:
    current_truck: Truck

    def animated_dots(self, duration, interval):
        """
        Display animated dots on the console for a specified duration.

        :param duration: The duration in seconds for which the animated dots should be displayed.
        :type duration: int
        :param interval: The time interval in seconds between each dot.
        :type interval: float
        :return: None
        """
        start_time = time.time()

        while time.time() - start_time < duration:
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(interval)

        print()

    def _start_day_process(self) -> None:
        """
        Start the day's process by taking input for the volume and weight of the truck's cargo,
        calling the `start_day` method of the `current_truck` object, displaying a loading animation,
        and printing a message indicating that the day has started.

        Inputs:
          - `current_truck`: an instance of the `Truck` class representing the truck for the day's process.

        Outputs:
          - None
        """
        volume = int(input("[?] Volume de carga em m³: "))
        weight = int(input("[?] Peso máximo da carga em kg: "))
        res = self.current_truck.start_day(volume, weight)
        print(res, end=" ")
        self.animated_dots(3, 0.25)
        print("Dia iniciado.")
        time.sleep(1)
        clear()
        return

    def _stop_process(self) -> None:
        """
        Manage the process of stopping the truck, including inserting and removing packages, and ending the stop.

        Inputs:
        - None

        Outputs:
        - None
        """
        clear()
        stop_menu = Menu(
            menu_text=[
                "1. Inserir pacote",
                "2. Retirar pacote",
                "3. Encerrar parada",
            ]
        )
        # Initialize a variable to keep track of the number of packages loaded at the current stop.
        packges_at_stop = 0

        while True:
            self.current_truck.stops += 1
            opt = stop_menu.run()
            if opt == 1:
                packge_weight = int(input("[?] Peso do pacote (em kg): "))
                packge_value = float(input("[?] Valor da mercadoria: "))
                print("Calculando custos", end=" ")
                self.animated_dots(3, 0.25)
                pack = Packge(packge_weight, packge_value)
                print(f"Custo do transporte: {pack.transport_cost}")
                extra_insurence = pack.extra_insurance_cost(
                    self.current_truck.volume)
                print(f"Custo de seguro: {extra_insurence}")
                if extra_insurence > 0:
                    opt_insurance = input(
                        "[?] Deseja inserir o custo de seguro? (s/n): ").lower()
                    if opt_insurance == "s":
                        print(
                            f"Custo total: {pack.transport_cost + extra_insurence}")
                        packge_value += extra_insurence
                        pack.value = packge_value
                    elif opt_insurance == "n":
                        print(
                            "O custo de seguro não foi inserido. Logo você precisa diminur o peso")
                        time.sleep(3)
                        continue
                    else:
                        print("Insira um valor válido!")
                        time.sleep(3)
                        continue
                confirmation = input(
                    "[?] Deseja inserir o pacote? (s/n): ").lower()
                if confirmation == "s":
                    res = self.current_truck.insert_package(pack)
                    packges_at_stop += 1
                    print(res)
                    time.sleep(5)
                    clear()
                    continue
                else:
                    print("O pacote não foi inserido.")
                    time.sleep(1)
                    continue

            elif opt == 2:
                print(f"""
                Aqui você pode retirar o seguinte pacote
                com as seguintes informações:
                Peso: {self.current_truck.load_list[-1].weight}
                Valor: {self.current_truck.load_list[-1].value}
                """)
                confirmation = input(
                    "[?] Deseja retirar o pacote? (s/n): ").lower()

                if confirmation == "s":
                    res = self.current_truck.remove_package()
                    print(res)
                    time.sleep(2)
                    clear()
                    continue
                else:
                    print("O pacote não foi retirado.")
                    time.sleep(2)
                    clear()
                    continue

            elif opt == 3:
                print("[!] Parada encerrada.")
                self.current_truck.qtd_packages_by_stop.append(
                    packges_at_stop
                )
                time.sleep(2)
                break
            else:
                print("Opção invalida. Por favor, escolha uma opção válida.")

    def _check_status_process(self) -> None:
        """
        Prints the current status of the truck, including the number of stops made, the total weight of the cargo, and the total value of the cargo.

        Example Usage:
        ```python
        run_program = RunProgram(current_truck)
        run_program._check_status_process()
        ```
        Expected Output:
        ```
        [!] Number of stops: 3
        [!] Total weight of cargo: 500 kg
        [!] Total value of cargo: $1000
        ```

        Inputs:
        - None

        Outputs:
        - None
        """
        situation = self.current_truck.situation
        for key, value in situation.items():
            print(f"[!] {key}: {value}")

    def _list_packages_process(self) -> None:
        """
        Prints a visual representation of the packages loaded in the current truck.

        Example Usage:
            run_program = RunProgram(current_truck)
            run_program._list_packages_process()

        Expected Output:
                             ▒
            ╔══════╦════╗▓
            ║▒▒▒▒▒▒║╦╦╦╦║▓
            ║▒▒▒▒▒▒║║║║║║▓
           █║▒▒▒▒▒█║║║║║║▓ [Package1, Package2, Package3]
         ╔╦╦╩══════╝╩╩╩╩║▓                                 ╔╗
         ║║║            ║▓─────────────────────────────────║║
         ║ºº••••••••••••╠══════════════════════════════════╝║
         ╚══════════════╝═══════════════════════════════════╝
           ( ☼ )   ( ☼ )                 ( ☼ )    ( ☼ )
            ºººº    ºººº                  ºººº     ºººº

        Inputs:
            - None

        Outputs:
            - None
        """
        print(f"""
                   ▒
      ╔══════╦════╗▓
      ║▒▒▒▒▒▒║╦╦╦╦║▓
      ║▒▒▒▒▒▒║║║║║║▓
     █║▒▒▒▒▒█║║║║║║▓ {self.current_truck.packages}
    ╔╦╦╩══════╝╩╩╩╩║▓                                 ╔╗
    ║║║            ║▓─────────────────────────────────║║
    ║ºº••••••••••••╠══════════════════════════════════╝║
    ╚══════════════╝═══════════════════════════════════╝
     ( ☼ )   ( ☼ )                 ( ☼ )    ( ☼ )
      ºººº    ºººº                   ººº       ººº
        """)

    def _end_day_process(self) -> None:
        """
        End the day's process by calling the `finish_day` method of the `current_truck` object,
        printing a message indicating that the day has ended, pausing for 2 seconds, and clearing the console screen.

        Example Usage:
        ```python
        run_program = RunProgram(current_truck)
        run_program._end_day_process()
        ```
        Expected Output:
        ```
        [!] Dia finalizado.
        ```
        """
        self.current_truck.finish_day()
        print("[!] Dia finalizado.")
        time.sleep(2)
        clear()

    def _generate_report_process(self) -> None:
        """
        Generates a report for the current truck by calling the `generate_report` method of the `current_truck` object.

        Example Usage:
        ```python
        run_program = RunProgram(current_truck)
        run_program._generate_report_process()
        ```
        Expected Output:
        ```
        [!] Gerando relatório.
        ... (loading animation)
        [!] Relatório gerado.
        ```

        Inputs:
        - None

        Flow:
        1. Print a message indicating that the report is being generated.
        2. Display an animated loading message.
        3. Call the `generate_report` method of the `current_truck` object.
        4. Pause for 2 seconds.
        5. Print a message indicating that the report has been generated.

        Outputs:
        - None
        """
        print("[!] Gerando relatório.")
        self.animated_dots(3, 0.25)
        self.current_truck.generate_report()
        time.sleep(2)
        print("[!] Relatório gerado.")
        clear()

    def run(self, choice: int) -> None:
        """
        Executes different processes based on the user's choice.

        Args:
            choice (int): The user's choice for the process to be executed.

        Returns:
            None

        Raises:
            None

        Example Usage:
            run_program = RunProgram(current_truck)
            run_program.run(1)

        Expected Output:
            The `_start_day_process` method is called.

        """
        if choice == 1:
            self._start_day_process()
        elif choice == 2:
            self._stop_process()
        elif choice == 3:
            self._check_status_process()
        elif choice == 4:
            self._list_packages_process()
        elif choice == 5:
            self._end_day_process()
        elif choice == 6:
            self._generate_report_process()
        elif choice == 7:
            print("[!] Saindo do programa", end=" ")
            self.animated_dots(3, 0.25)
            sys.exit(1)
        else:
            print("Opção invalida. Por favor, escolha uma opção válida.")
