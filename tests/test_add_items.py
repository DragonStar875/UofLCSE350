import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
from pantry_utils import update_user_pantry, get_user_pantry


@pytest.fixture
def userPantry():
    mock_database = {
        'item_name': ['butter', 'milk', 'tomato'],
        'quantity': [4, 2, 5],
        'exp_date': ['2025-07-11', '2026-10-01', '2027-02-03'],
        'threshold': [1, 1, 1]
    }

    return pd.DataFrame(mock_database)


@pytest.fixture
def allGroceries():
    mock_database = {
        'description': ['tomato', 'milk', 'pasta'],
        'foodPortionValue': [1, 1, 1],
        'foodPortionUnit': ['cup', 'cup', 'cup'],
        'price': [0.50, 1.20, 1.00]
    }

    return pd.DataFrame(mock_database)

def test_input_search_found(userPantry):
    query = "tomato"
    matches = userPantry[userPantry['item_name'].str.contains(query, case=False)]
    assert not matches.empty
    assert 'tomato' in matches['item_name'].values

def test_input_search_not_found(userPantry):
    query = "pudding"
    matches = userPantry[userPantry['item_name'].str.contains(query, case=False)]
    assert matches.empty

def test_add_new_item(userPantry, allGroceries):
    result = update_user_pantry(userPantry, allGroceries, 'pasta', 2)
    pantry_dict = get_user_pantry(userPantry)

    assert result.get("success") is not None
    assert any(item['item_name'].lower() == 'pasta' for item in pantry_dict)

def test_add_existing_item(userPantry, allGroceries):
    # Add item once
    update_user_pantry(userPantry, allGroceries, 'milk', 1)
    # Add item again
    result = update_user_pantry(userPantry, allGroceries, 'milk', 3)
    pantry_dict = get_user_pantry(userPantry)
    milk_entry = next(item for item in pantry_dict if item['item_name'].lower() == 'milk')

    assert result.get("success") is not None
    assert milk_entry['quantity'] == 6
    # 2(initial) + 1 + 3 = 6
