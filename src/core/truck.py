import re
from datetime import datetime
from dataclasses import dataclass, field
from typing import List

from core.decorators import day_started_required, are_there_packges_in_the_truck


@dataclass
class Packge:
    """
    Represents a package with weight and value attributes.
    Provides methods for calculating transport cost and extra insurance cost.
    """

    weight: int
    value: float

    def __str__(self) -> str:
        """
        Returns a string representation of the package in the format "|{weight}Kg|".
        """
        return f"|{self.weight}Kg|"

    def __repr__(self) -> str:
        """
        Returns a string representation of the package in the format "|{weight}Kg|".
        """
        return f"|{self.weight}Kg|"

    @property
    def transport_cost(self) -> float:
        """
        Calculates and returns the transport cost of the package based on its weight.
        """
        return self.weight * 1.50

    def extra_insurance_cost(self, truck_volume: int) -> float:
        """
        Calculates and returns the extra insurance cost of the package based on the truck volume.
        """
        return (
            (self.weight - truck_volume) *
            0.8 if truck_volume * 10 < self.weight else 0
        )


@dataclass
class Truck:
    """
    Represents a truck that can carry packages.
    
    Attributes
    ----------
    max_weight_setted : int
        The maximum weight set for the truck.
    volume : int
        The volume of the truck.
    current_day : bool
        Indicates if a day is currently in progress.
    current_capacity : int
        The current capacity of the truck.
    load_list : List[Packge]
        The list of packages loaded in the truck.
    stops : int
        The number of stops made by the truck.
    qtd_packages_by_stop : List[int]
        The list of quantities of packages at each stop.
    """

    max_weight_setted: int = 0
    volume: int = 0
    current_day: bool = False
    current_capacity: int = 0
    load_list: List[Packge] = field(default_factory=list)
    stops: int = 0
    qtd_packages_by_stop: List[int] = field(default_factory=list)

    def start_day(self, volume: int, weight: int) -> str:
        """
        Starts a new day with the given volume and weight.
        
        Parameters
        ----------
        volume : int
            The volume of the truck.
        weight : int
            The maximum weight set for the truck.
        
        Returns
        -------
        str
            A message indicating if the day was successfully started.
        """
        if self.current_day:
            return "Você já começou dia!"
        else:
            self.max_weight_setted = weight
            self.volume = volume
            self.current_day = True
            return "Começando dia"

    @day_started_required
    def insert_package(self, packge: Packge) -> str:
        """
        Inserts a package into the truck.
        
        Parameters
        ----------
        packge : Packge
            The package to be inserted.
        
        Returns
        -------
        str
            A message indicating if the package was successfully inserted.
        """
        self.load_list.append(packge)
        self.current_capacity += packge.weight
        return "Pacote inserido"

    @day_started_required
    @are_there_packges_in_the_truck
    def remove_package(self) -> str:
        """
        Removes the last package inserted into the truck.
        
        Returns
        -------
        str
            A message indicating if the package was successfully removed.
        """
        self.load_list.pop()
        return "Pacote removido"

    @property
    @day_started_required
    def situation(self) -> dict:
        """
        Retrieves information about the truck's situation.
        
        Returns
        -------
        dict
            A dictionary containing information about the truck's situation, including the current weight, remaining weight, maximum weight, number of loaded packages, remaining packages, maximum packages, transported value, remaining/excess value, and maximum transport cost.
        """
        current_weight = sum(packge.weight for packge in self.load_list)
        return {
            "Peso carregado": current_weight,
            "Peso restante": self.max_weight_setted - current_weight,
            "Peso máximo": self.max_weight_setted,
            "Quantidade de pacotes carregados": len(self.load_list),
            "Quantidade de pacotes restantes": self.max_weight_setted - current_weight,
            "Quantidade de pacotes máximo": self.max_weight_setted,
            "Valor trasportado": sum(packge.value for packge in self.load_list),
            "Valor restante ou excedente (mostrado em negativo)": sum(
                packge.value for packge in self.load_list
            )
            - sum(packge.transport_cost for packge in self.load_list),
            "Valor padrão máximo": sum(
                packge.transport_cost for packge in self.load_list
            ),
        }

    @property
    @day_started_required
    @are_there_packges_in_the_truck
    def packages(self) -> list:
        """
        Retrieves the list of packages in the truck.
        
        Returns
        -------
        list
            A list of packages in the truck.
        """
        return [f"{packge}" for packge in self.load_list]

    def finish_day(self) -> None:
        """
        Finishes the current day.
        """
        self.current_day = False

    @day_started_required
    @are_there_packges_in_the_truck
    def generate_report(self) -> None:
        """
        Generates a report with various parameters and saves it as an HTML file.
        """
        report_parameters = {
            "day": datetime.now().strftime("%d_%m_%Y"),
            "smallest_packge_weight": min(packge.weight for packge in self.load_list),
            "largest_packge_weight": max(packge.weight for packge in self.load_list),
            "smallest_quantity_of_packages": min(
                self.qtd_packages_by_stop
            ),
            "largest_quantity_of_packages": max(
                self.qtd_packages_by_stop
            ),
            "smallest_quantity_total_weight": self.current_capacity - self.volume,
            "largest_quantity_total_weight": self.current_capacity,
            "smallest_excess_weight_total": max(
                packge.transport_cost for packge in self.load_list
            ),
            "largest_excess_weight_total": max(
                packge.transport_cost for packge in self.load_list
            ),
            "labels": [packge.weight for packge in self.load_list],
            "data": [packge.transport_cost for packge in self.load_list],
        }

        with open("src/core/report_template.html", "r") as f:
            template = f.read()

        pattern = r"%\s*(.*?)\s*%"
        matches = re.findall(pattern, template, re.MULTILINE)
        for match in matches:
            template = template.replace(
                f"% {match} %", str(report_parameters[match]))

        try:
            with open(f"relatorio_{report_parameters['day']}.html", "w") as f:
                f.write(template)
        except Exception as e:
            print(e)
