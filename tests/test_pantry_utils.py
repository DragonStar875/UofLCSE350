import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pantry_utils import get_nutrition, threshold_checker

import pytest
from pantry_utils import get_nutrition, threshold_checker

# Sample mock data for allGroceries
import pandas as pd

mock_data = pd.DataFrame([
    {
        'description': 'Hummus, commercial',
        'category': 'Legumes and Legume Products',
        'calories': 166,
        'carbohydrates': 14.9,
        'protein': 7.35,
        'fat': 17.1
    }
])

def test_get_nutrition_exact_match():
    result = get_nutrition(mock_data, 'Hummus, commercial')
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]['description'] == 'Hummus, commercial'


def test_get_nutrition_partial_match():
    result = get_nutrition(mock_data, 'hummus')
    assert isinstance(result, list)
    assert len(result) >= 1


def test_threshold_checker_below_threshold():
    pantry_df = pd.DataFrame([
        {'item_name': 'Hummus, commercial', 'quantity': 1, 'threshold': 2}
    ])
    result = threshold_checker(pantry_df)
    assert isinstance(result, list)
    assert result == [{'item_name': 'Hummus, commercial', 'quantity': 1, 'threshold': 2}]


def test_threshold_checker_above_threshold():
    pantry_df = pd.DataFrame([
        {'item_name': 'Hummus, commercial', 'quantity': 3, 'threshold': 2}
    ])
    result = threshold_checker(pantry_df)
    assert result == []