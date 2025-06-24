import pandas as pd

# import userPantry
userPantry = pd.read_csv('userPantry.csv')

# import allGroceries
allGroceries = pd.read_csv('allGroceries.csv')

def get_price(allGroceries, food_name):
    return allGroceries.loc[allGroceries['item_name'] == food_name, ['food_name','quantity', 'price']]