import logging
from abc import (ABC, abstractmethod)
from functools import reduce
from typing import (List, Tuple)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class AbstractNumberProcessor(ABC):
    @abstractmethod
    def filter_even(self) -> List[int]:
        pass

    @abstractmethod
    def square_numbers(self) -> List[int]:
        pass

    @abstractmethod
    def sum_numbers(self) -> int:
        pass


class NumberProcessor(AbstractNumberProcessor):
    def __init__(self, numbers: List[int]):
        self.numbers: List[int] = numbers
        logging.info(f'Initialized NumberProcessor with numbers: {self.numbers}')

    def filter_even(self) -> List[int]:
        """Return a list of even numbers."""
        even_numbers = list(filter(lambda x: x % 2 == 0, self.numbers))
        logging.info(f'Filtered even numbers: {even_numbers}')
        return even_numbers

    def square_numbers(self) -> List[int]:
        """Return a list of squared numbers."""
        squared_numbers = list(map(lambda x: x ** 2, self.numbers))
        logging.info(f'Squared numbers: {squared_numbers}')
        return squared_numbers

    def sum_numbers(self) -> int:
        """Return the sum of the numbers."""
        summed = reduce(lambda x, y: x + y, self.numbers)
        logging.info(f'Sum of numbers: {summed}')
        return summed


class AbstractCoordinateSorter(ABC):
    @abstractmethod
    def sort_by_latitude(self, reverse: bool = False) -> List[Tuple[float, float]]:
        pass


class CoordinateSorter(AbstractCoordinateSorter):
    def __init__(self, coordinates: List[Tuple[float, float]]):
        self.coordinates: List[Tuple[float, float]] = coordinates
        logging.info(f'Initialized CoordinateSorter with coordinates: {self.coordinates}')

    def sort_by_latitude(self, reverse: bool = False) -> List[Tuple[float, float]]:
        """Return coordinates sorted by latitude."""
        sorted_coords = sorted(self.coordinates, key=lambda x: x[0], reverse=reverse)
        logging.info(f'Sorted coordinates: {sorted_coords} (reverse={reverse})')
        return sorted_coords


# Example usage
if __name__ == "__main__":
    nums: List[int] = [1, 2, 3, 4, 5]
    num_processor = NumberProcessor(nums)

    even_nums: List[int] = num_processor.filter_even()
    print('Even numbers:', even_nums)

    squared_nums: List[int] = num_processor.square_numbers()
    print('Squared numbers:', squared_nums)

    reduce_summed: int = num_processor.sum_numbers()
    print('Reduce (sum):', reduce_summed)

    coordinates: List[Tuple[float, float]] = [(23.45, -45.9), (19.59, 59.9), (10.45, -9.91)]
    coord_sorter = CoordinateSorter(coordinates)

    sorted_coordinates: List[Tuple[float, float]] = coord_sorter.sort_by_latitude(reverse=True)
    print('Coordinates:', coordinates)
    print('Sorted coordinates:', sorted_coordinates)
