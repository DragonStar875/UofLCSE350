import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    assert result[0]['calories'] == 166

    result = get_nutrition(mock_data, 'Gold')
    assert isinstance(result, dict)
    assert 'error' in result
    assert result['error'] == "Item 'Gold' cannot be found."


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

def test_get_user_pantry():
    from pantry_utils import get_user_pantry

    df = pd.DataFrame([
        {'item_name': 'Oats', 'quantity': 2, 'threshold': 1},
        {'item_name': 'Chickpeas', 'quantity': 1, 'threshold': 2}
    ])

    records = get_user_pantry(df)

    assert isinstance(records, list)
    assert len(records) == 2
    assert records[0]['item_name'] == 'Oats'


def test_get_expired_items():
    from pantry_utils import get_expired_items

    items = [
        {'item_name': 'Oats', 'quantity': 2, 'threshold': 1, 'exp_date': '2025-09-15'},
        {'item_name': 'Chickpeas', 'quantity': 1, 'threshold': 2, 'exp_date': '2025-05-15'}
    ]

    expired = get_expired_items(items)

    assert isinstance(expired, list)
    assert len(expired) == 1
    assert expired[0]['item_name'] == 'Chickpeas'


def test_sort_user_pantry():
    from pantry_utils import sort_user_pantry

    df = pd.DataFrame([
        {'item_name': 'Oats', 'quantity': 2, 'threshold': 1},
        {'item_name': 'Chickpeas', 'quantity': 1, 'threshold': 2}
    ])

    sorted_records = sort_user_pantry(df, 'item_name')

    assert isinstance(sorted_records, list)
    assert len(sorted_records) == 2
    assert sorted_records[0]['item_name'] == 'Oats'

