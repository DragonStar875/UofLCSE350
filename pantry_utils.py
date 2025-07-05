import pandas as pd

def load_csvs():
    userPantry = pd.read_csv('userPantry.csv')
    shoppingList = pd.read_csv('shoppingList.csv')
    allGroceries = pd.read_csv('allGroceries.csv')
    return userPantry, shoppingList, allGroceries


def threshold_checker(userPantry):
    below_threshold = userPantry[userPantry['quantity'] < userPantry['threshold']]
    if below_threshold.empty:
        return []
    return below_threshold[['item_name', 'quantity', 'threshold']].to_dict('records')


def get_nutrition(allGroceries, food_name):
    try:
        df = allGroceries[allGroceries['description'].str.lower().str.contains(food_name.lower())]
        if df.empty:
            return None
        return df.to_dict('records')
    except Exception as e:
        return {"error": str(e)}


def get_price(allGroceries, food_name):
    try:
        df = allGroceries[allGroceries['description'].str.lower().str.contains(food_name.lower())]
        if df.empty:
            return None
        return df[['description', 'foodPortionValue','foodPortionUnit', 'price']].to_dict('records')
    except Exception as e:
        return {"error": str(e)}


def get_shopping_list(shoppingList):
    return shoppingList.to_dict('records')


def update_shopping_list(shoppingList, food_name):
    if food_name in shoppingList['item_name'].values:
        return shoppingList, f"{food_name} is already in the shopping list."

    new_row = pd.DataFrame([{'item_name': food_name}])
    updated_list = pd.concat([shoppingList, new_row], ignore_index=True)
    return updated_list, f"{food_name} added to the shopping list."


def get_user_pantry(userPantry):
    return userPantry.to_dict('records')


def closeout(userPantry, shoppingList):
    try:
        userPantry.to_csv("userPantry.csv", index=False)
        shoppingList.to_csv("shoppingList.csv", index=False)
        return "Changes successfully saved."
    except Exception as e:
        return f"Error saving data: {e}"
