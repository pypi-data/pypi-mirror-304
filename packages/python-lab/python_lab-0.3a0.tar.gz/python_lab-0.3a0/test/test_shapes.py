import pytest

from src.main import NumberProcessor, CoordinateSorter


def test_number_processor():
    nums = [1, 2, 3, 4, 5]
    processor = NumberProcessor(nums)

    # Test filter_even
    assert processor.filter_even() == [2, 4]

    # Test square_numbers
    assert processor.square_numbers() == [1, 4, 9, 16, 25]

    # Test sum_numbers
    assert processor.sum_numbers() == 15


def test_coordinate_sorter():
    coordinates = [(23.45, -45.9), (19.59, 59.9), (10.45, -9.91)]
    sorter = CoordinateSorter(coordinates)

    # Test sort_by_latitude with reverse=True
    sorted_coordinates_desc = sorter.sort_by_latitude(reverse=True)
    assert sorted_coordinates_desc == [(23.45, -45.9), (19.59, 59.9), (10.45, -9.91)]

    # Test sort_by_latitude with reverse=False
    sorted_coordinates_asc = sorter.sort_by_latitude(reverse=False)
    assert sorted_coordinates_asc == [(10.45, -9.91), (19.59, 59.9), (23.45, -45.9)]


if __name__ == "__main__":
    pytest.main()
