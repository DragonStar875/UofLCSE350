import pandas as pd


userPantry = pd.read_csv('userPantry.csv')

def set_critical(userPantry, food_name, critical_value):
    userPantry.loc[userPantry['item_name'] == food_name, 'critical_threshold'] = critical_value
    return