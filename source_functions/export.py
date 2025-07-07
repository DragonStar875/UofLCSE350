import pandas as pd

# overwrite dataframe to csv's
shoppingList = pd.read_csv('../shoppingList.csv')

# export shopping list to export.csv
def exportShoppingList():
    try:
        shoppingList.to_csv('../export.csv', index=False)
        print("Shopping list exported!")
    except Exception as e:
        print(f"Error exporting: {e}")
