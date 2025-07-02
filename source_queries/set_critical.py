import pandas as pd


userPantry = pd.read_csv('userPantry.csv')
"""
Incorporated into smartShelf.py
Function needs some kind of success/fail return value
and a try/catch block for critical_value, that determines if it is an int, non-negative, and not preposterously large 
"""
def set_critical(userPantry, food_name, critical_value):
    userPantry.loc[userPantry['item_name'] == food_name, 'critical_threshold'] = critical_value
    return