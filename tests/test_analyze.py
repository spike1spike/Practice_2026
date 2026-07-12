import pytest
from src.analyze import Analyzer

# Fixtures

@pytest.fixture
def default_phone():
    return {
        'rating_normalized': 0.5,
        'has_5g': 0,
        'has_nfc': 0,
        'has_ir_blaster': 0,
        'processor_speed_normalized': 0.8,
        'battery_capacity_normalized': 0.25,
        'fast_charging_normalized': 0.7,
        'ram_capacity_normalized': 0.75,
        'internal_memory_normalized': 0.5,
        'refresh_rate_normalized': 0.9,
        'primary_camera_rear_normalized': 0.8,
        'primary_camera_front_normalized': 0.25,
        'extended_upto_normalized': 0.75,
        'ppi_normalized': 0.9
    }

@pytest.fixture
def pricevalue_phone():
    return {
            'price_normalized': 0.8,
            'value_score': 0.65
        }

# Tests

def test_calc_valuescore(default_phone):
    actual = Analyzer.calc_valuescore(table = default_phone)
    expected = 0.6035

    assert actual == pytest.approx(expected, abs = 1e-6)

def test_calc_pricevalue(pricevalue_phone):
    actual = Analyzer.calc_pricevalue(table = pricevalue_phone)
    expected = 537.5
    
    assert actual == pytest.approx(expected, abs = 1e-6)

@pytest.mark.parametrize('column, smaller_value, greater_value', [
    ('rating_normalized', 0.5, 0.6),
    ('has_5g', 0, 1),
    ('has_nfc', 0, 1),
    ('has_ir_blaster', 0, 1),
    ('processor_speed_normalized', 0.8, 0.9),
    ('battery_capacity_normalized', 0.25, 0.35),
    ('fast_charging_normalized', 0.7, 0.8),
    ('ram_capacity_normalized', 0.75, 0.85),
    ('internal_memory_normalized', 0.5, 0.6),
    ('refresh_rate_normalized', 0.9, 1),
    ('primary_camera_rear_normalized', 0.8, 0.9),
    ('primary_camera_front_normalized', 0.25, 0.35),
    ('extended_upto_normalized', 0.75, 0.85),
    ('ppi_normalized', 0.9, 1)
])
def test_change_valuescore(default_phone, column, smaller_value, greater_value):
    phone_a = default_phone.copy()
    phone_b = default_phone.copy()

    phone_a[column] = smaller_value
    phone_b[column] = greater_value

    value_a = Analyzer.calc_valuescore(table = phone_a)
    value_b = Analyzer.calc_valuescore(table = phone_b)

    assert value_a < value_b