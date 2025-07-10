# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#
# import pytest
# from source_functions.priceQuery import get_price
#
# import pandas as pd
#
# @pytest.fixture
# def mock_database():
#     data = {
#         'item_name': ['apple', 'banana', 'carrot', 'eggs', 'ham', 'cream', 'rice', 'spinach', 'tomatoes', 'watermelon', 'yogurt'],
#         'quantity': [2, 4, 2, 12, 1, 12, 2, 3, 4, 1, 1],
#         'price': [1.30, 0.97, None, 0.60, 1.74, 0.36, 0.25, 0.48, 0.41, None, 0.89],
#         'category': ['produce', 'produce', 'produce', 'dairy', 'meat', 'dairy', 'grains', 'produce', 'produce', 'produce', 'dairy']
#     }
#
#     return pd.DataFrame(data)
#
# def test_price_found(mock_database):
#     price = get_price(mock_database, 'rice')
#     assert price == 0.25
#
# def test_price_missing(mock_database):
#     price = get_price(mock_database, 'carrot')
#     assert price is None
#
# def test_price_not_found(mock_database):
#     price = get_price(mock_database, 'tofu')
#     assert price is None
