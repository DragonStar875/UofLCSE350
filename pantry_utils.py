import pandas as pd
from pywebio.input import NUMBER, input as pw_input
from pywebio.output import put_success, clear_scope, put_error


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

def prompt_add_qty(description, userPantry, allGroceries):
    qty = pw_input(f"Enter quantity to add for '{description}':", type=NUMBER, required=True)

    result = update_user_pantry(userPantry, allGroceries, description, qty)
    clear_scope('main')  # Clear the old table

    if isinstance(result, dict) and result.get("error"):
        put_error(f"Error: {result['error']}", scope='main')
    else:

        put_success(result.get("success", f"Added {qty} of {description} to pantry."), scope='main')


def update_user_pantry(userPantry, allGroceries, food_name, qty):
    try:
        # Match item from allGroceries
        df = allGroceries[allGroceries['description'].str.lower().str.contains(food_name.lower())]
        if df.empty:
            return {"error": f"Item '{food_name}' not found in grocery list."}

        item = df.iloc[0]
        item_name = item['description']

        # Try to find an existing row by item_name
        existing = userPantry[userPantry['item_name'].str.lower() == item_name.lower()]

        if not existing.empty:
            idx = existing.index[0]
            userPantry.at[idx, 'quantity'] += qty
        else:
            new_row = {
                'item_name': item_name,
                'quantity': qty,
                'exp_date': '',  # or use a default like datetime.today() + timedelta(...)
                'threshold': 0   # optionally set a default threshold
            }
            userPantry.loc[len(userPantry)] = new_row

        return {"success": f"Updated pantry with {qty} of {item_name}."}
    except Exception as e:
        return {"error": str(e)}


def get_user_pantry(userPantry):
    return userPantry.to_dict('records')

def sort_user_pantry(userPantry, sortChoice):
    return userPantry.sort_values(by=[sortChoice], ascending=False).to_dict('records')

def closeout(userPantry, shoppingList):
    try:
        userPantry.to_csv("userPantry.csv", index=False)
        shoppingList.to_csv("shoppingList.csv", index=False)
        return "Changes successfully saved."
    except Exception as e:
        return f"Error saving data: {e}"
