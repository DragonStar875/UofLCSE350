import pandas as pd

userPantry = pd.read_csv('userPantry.csv')

def pantryQuery(userPantry, food_name):
    result = userPantry.loc[userPantry['item_name'] == food_name, ['quantity', 'critical_threshold']]
        if result.empty:
            return "Item cannot be found"
    return result