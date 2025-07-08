import pandas as pd

# import userPantry
userPantry = pd.read_csv('userPantry.csv')

# import allGroceries
allGroceries = pd.read_csv('allGroceries.csv')

def get_price(allGroceries, food_name):
    result = allGroceries.loc[allGroceries['item_name'] == food_name, ['item_name','quantity', 'price']]
    if result.empty:
        return None

    price = result.iloc[0]['price']
    if pd.isna(price):
        return None
    return price
