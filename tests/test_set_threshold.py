import pytest
import pandas as pd
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pantry_utils import update_user_pantry

@pytest.fixture
def sample_pantry():
    return pd.DataFrame({
        'item_name': ['apple'],
        'quantity': [2],
        'exp_date': [''],
        'threshold': [5]
    })

@pytest.fixture
def all_groceries():
    return pd.DataFrame({
        'description': ['apple', 'banana'],
        'category': ['produce', 'produce'],
        'price': [1.0, 0.5]
    })

def test_threshold_unchanged_for_existing(sample_pantry, all_groceries):
    update_user_pantry(sample_pantry, all_groceries, 'apple', 1)
    assert sample_pantry.loc[sample_pantry['item_name'] == 'apple', 'threshold'].values[0] == 5

def test_threshold_default_for_new_item(sample_pantry, all_groceries):
    update_user_pantry(sample_pantry, all_groceries, 'banana', 3)
    threshold = sample_pantry.loc[sample_pantry['item_name'] == 'banana', 'threshold'].values[0]
    assert threshold == 0
