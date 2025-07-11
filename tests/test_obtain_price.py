import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from pantry_utils import get_price

import pandas as pd

@pytest.fixture
def mock_database():
    mock_database = {
        'description': ['apple', 'banana', 'carrot', 'eggs', 'ham', 'cream', 'rice', 'spinach', 'tomatoes', 'watermelon', 'yogurt'],
        'foodPortionValue': [2, 4, 2, 12, 1, 12, 2, 3, 4, 1, 1],
        'foodPortionUnit': ['piece', 'piece', 'cup', 'oz', 'slice', 'tbsp', 'cup', 'bunch', 'cup', 'slice', 'cup'],
        'price': [1.30, 0.97, None, 0.60, 1.74, 0.36, 0.25, 0.48, 0.41, None, 0.89]
    }

    return pd.DataFrame(mock_database)

def test_price_found(mock_database):
    result = get_price(mock_database, 'rice')
    assert isinstance(result, list)
    assert result[0]['price'] == 0.25

def test_price_missing(mock_database):
    result = get_price(mock_database, 'carrot')
    assert isinstance(result, list)
    assert pd.isna(result[0]['price'])

def test_price_not_found(mock_database):
    result = get_price(mock_database, 'tofu')
    assert result is None
