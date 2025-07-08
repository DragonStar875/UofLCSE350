import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from source_functions.priceQuery import get_price

import pandas as pd

@pytest.fixture
def mock_database():
    data = {
        'item_name': ['butter', 'broccoli', 'granola', 'ketchup', 'milk', 'pickle', 'rasberry', 'sweet potato', 'tofu', 'tomato', 'zucchini'],
        'quantity': [4, 5, 2, 1, 2, 4, 6, 2, 3, 5, 3],
        'expiration_date': [
            '2025-07-11', '2025-08-01', '2025-07-15', '2024-01-16', '2026-10-01', '2025-09-26', '2027-03-05', '2026-02-28', '2025-12-20', '2027-02-03', '2026-04-09'],
        'category': ['dairy', 'produce', 'grains', 'other', 'dairy', 'other', 'produce', 'produce', 'protein', 'produce', 'produce']
    }

    return pd.DataFrame(data)

def test_input_search_found(mock_database):
    query = "tomato"
    matches = mock_database[mock_database['item_name'].str.contains(query, case=False)]
    assert not matches.empty
    assert 'tomato' in matches['item_name'].values

def test_input_search_not_found(mock_database):
    query = "pudding"
    matches = mock_database[mock_database['item_name'].str.contains(query, case=False)]
    assert matches.empty

def test_add_items(mock_database):
    new_item = {
        'item_name': 'pasta',
        'quantity': 2,
        'expiration_date': '2025-07-15',
        'category': 'grains'
    }

    initial_length = len(mock_database)
    mock_database.loc[len(mock_database)] = new_item
    updated_length = len(mock_database)

    assert updated_length == initial_length + 1
    assert 'pasta' in mock_database['item_name'].values
