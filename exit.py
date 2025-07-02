import pandas as pd
import sys

# overwrite dataframe to csv's
userPantry = pd.read_csv('userPantry.csv')
shoppingList = pd.read_csv('shoppingList.csv')
allGroceries = pd.read_csv('allGroceries.csv')

# update userPantry, shoppingList, allGroceries
def exitProgram (userPantry, shoppingList, allGroceries):
    try:
        userPantry.to_csv("userPantry.csv", index=False)
        shoppingList.to_csv("shoppingList.csv", index=False)
        allGroceries.to_csv("allGroceries.csv", index=False)
        print("All data saved! Exiting program!")
    except Exception as e:
        print(f"Error saving data: {e}")
    sys.exit()