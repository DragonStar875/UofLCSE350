import pytest, pandas as pd, sys, os

from source_functions.set_critical import set_critical




@pytest.fixture
def sample_data():
    data = {
        'item_name': ['apple', 'banana', 'carrot', 'eggs', 'ham', 'cream', 'rice', 'spinach', 'tomatoes', 'watermelon', 'yogurt'],
        'quantity': [2, 4, 2, 12, 1, 12, 2, 3, 4, 1, 1],
        'price': [1.30, 0.97, None, 0.60, 1.74, 0.36, 0.25, 0.48, 0.41, None, 0.89],
        'category': ['produce', 'produce', 'produce', 'dairy', 'meat', 'dairy', 'grains', 'produce', 'produce', 'produce', 'dairy'],
        'threshold': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }

    return pd.DataFrame(data)

@pytest.fixture
def empty_data():
    return pd.DataFrame()

def test_set_threshold(sample_data):
    result = set_critical(sample_data, 'apple', 2)
    assert(result == "Threshold for apple was set to 2, checking critical values.")

def test_set_item_not_found(empty_data):
    result = set_critical(empty_data, 'apple', 2)
    assert(result == "Failed to gather userPantry.csv, check for path or missing data error.")

def test_set_item_too_high(sample_data):
    result = set_critical(sample_data, 'apple', 101)
    assert(result == "Error: Please ensure that your critical value is less than 100.")

def test_set_item_negative(sample_data):
    result = set_critical(sample_data, 'apple', -1)
    assert(result == "Error: Please ensure that your critical value is positive.")

