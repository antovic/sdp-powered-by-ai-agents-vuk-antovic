# INPUT-BE-004.1 / INPUT-BE-004.2: Grid configuration validation
import pytest
from src.rover import Grid


def test_input_be_004_1_s1_negative_dimension_raises_value_error():
    # GIVEN / WHEN / THEN
    with pytest.raises(ValueError, match="Grid width must be positive"):
        Grid(width=-5, height=5)


def test_input_be_004_2_s1_out_of_bounds_obstacle_raises_value_error():
    # GIVEN / WHEN / THEN
    with pytest.raises(ValueError, match=r"Obstacle at \(6,1\) is outside grid bounds \(5x5\)"):
        Grid(width=5, height=5, obstacles={(6, 1)})
