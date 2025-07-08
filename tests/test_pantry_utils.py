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

def test_get_user_pantry(tmp_path):
    # Create a temporary CSV file to simulate userPantry.csv
    test_data = pd.DataFrame([
        {'item_name': 'Oats', 'quantity': 2, 'threshold': 1},
        {'item_name': 'Chickpeas', 'quantity': 1, 'threshold': 2}
    ])
    test_file = tmp_path / "userPantry.csv"
    test_data.to_csv(test_file, index=False)

    from pantry_utils import get_user_pantry  # Assumes this function exists

    df = get_user_pantry(test_file)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 3)
    assert 'item_name' in df.columns
    assert df.iloc[0]['item_name'] == 'Oats'


def test_sort_user_pantry(tmp_path):
    test_data = pd.DataFrame([
        {'item_name': 'Oats', 'quantity': 2, 'threshold': 1},
        {'item_name': 'Chickpeas', 'quantity': 1, 'threshold': 2}
    ])
    test_file = tmp_path / "userPantry.csv"
    test_data.to_csv(test_file, index=False)

    from pantry_utils import get_user_pantry, sort_user_pantry  # Assumes both exist

    df = get_user_pantry(test_file)
    sorted_df = sort_user_pantry(df, 'item_name')

    assert isinstance(sorted_df, pd.DataFrame)
    assert sorted_df.iloc[0]['item_name'] == 'Chickpeas'  # Alphabetical sort
