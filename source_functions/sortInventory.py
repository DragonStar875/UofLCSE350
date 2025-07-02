import pandas as pd

#import userPantry
userPantry = pd.read_csv('../userPantry.csv')

#import shoppingList
shoppingList = pd.read_csv('../shoppingList.csv')

#import allGroceries
allGroceries = pd.read_csv('allGroceries.csv')

def sortInv(inventory, sort_by='item_name', ascending=True):
    valid_columns = inventory.columns.tolist()
    
    if sort_by not in valid_columns:
        return f"Invalid sort criteria. Please choose from: {', '.join(valid_columns)}"
    
    try:
        sorted_df = inventory.sort_values(by=sort_by, ascending=ascending)
        return sorted_df.to_dict('records')
    except Exception as e:
        return f"An error occurred while sorting: {e}"