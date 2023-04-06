import pytest
import calculators.simple_calc.simple_calc as calc

def test_execute():
    assert calc.execute() == 2
