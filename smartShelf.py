from pywebio import start_server
from pywebio.input import input_group, input, NUMBER, select, actions
from pywebio.output import (put_table, put_text, put_success, put_error, put_buttons, put_scope, use_scope, clear_scope)
from pantry_utils import (
    load_csvs, threshold_checker, get_nutrition, get_price,
    get_shopping_list, update_shopping_list,
    get_user_pantry, closeout, update_user_pantry,
    sort_user_pantry, export_csv, get_expired_items
)
import re

# === Load data ===
userPantry, shoppingList, allGroceries = load_csvs()


def render_pantry():
    clear_scope('main')

    data = get_user_pantry(userPantry)

    if not data:
        put_text("Pantry is empty.", scope='main')
        return

    with use_scope('main'):
        # Ask user if they want to sort
        user_action = actions(label="Choose an action", buttons=[
            {'label': 'View Pantry', 'value': 'view'},
            {'label': 'Sort Pantry', 'value': 'sort'}
        ])

        if user_action == 'sort':
            sort_column = select("Select column to sort by:", options=list(data[0].keys()))
            sorted_data = sort_user_pantry(userPantry, sort_column)
            data_to_display = sorted_data
            put_text(f"Pantry sorted by: {sort_column}")
        else:
            data_to_display = data

        put_text("Current Pantry:")
        put_table([list(data_to_display[0].keys())] + [list(d.values()) for d in data_to_display])

def render_edit_pantry():
        clear_scope('main')
        # Prepare quantity update form
        inputs = []
        name_map = {}

        data = get_user_pantry(userPantry)

        for item in data:
            safe_name = re.sub(r'\W+', '_', item['item_name'])
            name_map[safe_name] = item['item_name']
            inputs.append(
                input(f"{item['item_name']} (current qty: {item['quantity']})",
                      name=safe_name, type=NUMBER, placeholder="Leave blank to skip")
            )

        form_data = input_group("Update Item Quantities", inputs)

        changes_made = False
        for safe_name, val in form_data.items():
            original_name = name_map[safe_name]
            if val is not None:
                try:
                    qty_val = int(val)
                    if qty_val < 0:
                        put_error(f"Invalid quantity for {original_name}: must be ≥ 0")
                    else:
                        userPantry.loc[userPantry['item_name'] == original_name, 'quantity'] = qty_val
                        changes_made = True
                except ValueError:
                    put_error(f"Invalid input for {original_name}: must be an integer")

        if changes_made:
            put_success("Quantities updated.")
        else:
            put_text("No quantities were changed.")

def render_thresholds_update():
    clear_scope('main')
    low_items = threshold_checker(userPantry)

    if not low_items:
        put_success("All items are above threshold.", scope='main')
        return

    put_table([list(low_items[0].keys())] + [list(d.values()) for d in low_items], scope='main')

    # Create safe input names and build a mapping
    inputs = []
    name_map = {}

    for item in low_items:
        safe_name = re.sub(r'\W+', '_', item['item_name'])
        name_map[safe_name] = item['item_name']
        inputs.append(
            input(f"{item['item_name']} (current threshold: {item['threshold']})",
                  name=safe_name, type=NUMBER, placeholder="Leave blank to skip")
        )

    form_data = input_group("Update Thresholds", inputs)

    changes_made = False
    for safe_name, val in form_data.items():
        original_name = name_map[safe_name]
        if val is not None:
            try:
                threshold_val = int(val)
                if threshold_val < 0 or threshold_val > 1000:
                    put_error(f"Invalid threshold for {original_name}: must be 0–1000", scope='main')
                else:
                    userPantry.loc[userPantry['item_name'] == original_name, 'threshold'] = threshold_val
                    changes_made = True
            except ValueError:
                put_error(f"Invalid input for {original_name}: must be an integer", scope='main')

    if changes_made:
        put_success("Thresholds updated.", scope='main')
    else:
        put_text("No thresholds were changed.", scope='main')

def render_set_exp():
    clear_scope('main')

    data = get_user_pantry(userPantry)
    if not data:
        put_text("Pantry is empty.", scope='main')
        return

    with use_scope('main'):

        # Prepare input fields for exp_date updates
        inputs = []
        name_map = {}

        for item in data:
            safe_name = re.sub(r'\W+', '_', item['item_name'])
            name_map[safe_name] = item['item_name']
            inputs.append(
                input(f"{item['item_name']} (current: {item['exp_date']})",
                      name=safe_name,
                      type="text",
                      placeholder="YYYY-MM-DD")
            )

        form_data = input_group("Update Expiration Dates", inputs)

        changes_made = False
        for safe_name, val in form_data.items():
            original_name = name_map[safe_name]
            if val:
                # Validate date format
                if re.fullmatch(r'\d{4}-\d{2}-\d{2}', val):
                    try:
                        # Check actual date validity
                        from datetime import datetime
                        datetime.strptime(val, '%Y-%m-%d')
                        userPantry.loc[userPantry['item_name'] == original_name, 'exp_date'] = val
                        changes_made = True
                    except ValueError:
                        put_error(f"Invalid date for {original_name}: {val} is not a real calendar date")
                else:
                    put_error(f"Invalid format for {original_name}: use YYYY-MM-DD")

        if changes_made:
            put_success("Expiration dates updated.")
        else:
            put_text("No expiration dates were changed.")


def render_expired_items():
    clear_scope('main')

    data = get_user_pantry(userPantry)

    if not data:
        put_text("Pantry is empty.", scope='main')
        return

    expired = get_expired_items(data)

    with use_scope('main'):
        if not expired:
            put_text("No expired items.")
            return

        put_text("Expired Items:")
        put_table([list(expired[0].keys())] + [list(d.values()) for d in expired])

"""

Nutrition lookups are working now!  Woohoo!  And it checks for df['description'].contains(food_name) so cheese returns a lot of rows :D
"""
def render_nutrition():
    clear_scope('main')
    food = input("Enter item name to get nutrition:")
    result = get_nutrition(allGroceries, food)

    if isinstance(result, dict) and result.get("error"):
        put_error(f"Error: {result['error']}", scope='main')
    else:
        put_table([list(result[0].keys())] + [list(r.values()) for r in result], scope='main')

def render_price_lookup():
    clear_scope('main')
    food = input("Enter item name to get price:")
    result = get_price(allGroceries, food)
    if not result:
        put_error("Item not found in grocery database.", scope='main')
    elif isinstance(result, dict) and result.get("error"):
        put_error(f"Error: {result['error']}", scope='main')
    else:
        put_table([list(result[0].keys())] + [list(r.values()) for r in result], scope='main')

def render_shopping_list():
    clear_scope('main')
    data = get_shopping_list(shoppingList)
    if not data:
        put_text("Shopping list is empty.", scope='main')
    else:
        put_table([list(data[0].keys())] + [list(d.values()) for d in data], scope='main')

def render_add_to_shopping():
    clear_scope('main')
    global shoppingList
    item = input("Enter item name to add to shopping list:")
    shoppingList, msg = update_shopping_list(shoppingList, item)
    put_success(msg, scope='main')

def render_edit_shopping_list():
    clear_scope('main')
    inputs = []
    name_map = {}

    data = shoppingList.to_dict('records')  # Assumes shoppingList is a pandas DataFrame

    for item in data:
        safe_name = re.sub(r'\W+', '_', item['item_name'])
        name_map[safe_name] = item['item_name']
        inputs.append(
            input(f"{item['item_name']} (current qty: {item['quantity']})",
                  name=safe_name, type=NUMBER, placeholder="Leave blank to skip")
        )

    form_data = input_group("Update Shopping List Quantities", inputs)

    changes_made = False
    for safe_name, val in form_data.items():
        original_name = name_map[safe_name]
        if val is not None:
            try:
                qty_val = int(val)
                if qty_val < 0:
                    put_error(f"Invalid quantity for {original_name}: must be ≥ 0")
                else:
                    if qty_val == 0:
                        # Remove item from shoppingList
                        shoppingList.drop(
                            shoppingList[shoppingList['item_name'] == original_name].index,
                            inplace=True
                        )
                    else:
                        # Update item quantity
                        shoppingList.loc[
                            shoppingList['item_name'] == original_name, 'quantity'
                        ] = qty_val
                    changes_made = True
            except ValueError:
                put_error(f"Invalid input for {original_name}: must be an integer")

    if changes_made:
        put_success("Shopping list updated.")
    else:
        put_text("No changes were made to the shopping list.")


def render_pantry_update():
    clear_scope('main')
    food_query = input("Enter food name to add to pantry:", required=True)

    matches = get_price(allGroceries, food_query)
    if not matches:
        put_error("No matching items found.", scope='main')
        return
    elif isinstance(matches, dict) and matches.get("error"):
        put_error(f"Error: {matches['error']}", scope='main')
        return

    def handle_add(item):
        qty = input(f"Enter quantity to add for '{item['description']}':", type=NUMBER, required=True)
        result = update_user_pantry(userPantry, allGroceries, item['description'], qty)
        clear_scope('main')
        if isinstance(result, dict) and result.get("error"):
            put_error(f"Error: {result['error']}", scope='main')
        else:
            put_success(f"Added {qty} of {item['description']} to pantry.", scope='main')
        render_pantry()

    with use_scope('main'):
        put_text("Select an item to add to pantry:")
        headers = ['Description', 'Portion Size', 'Unit', 'Price', '']
        rows = [
            [
                item['description'],
                item['foodPortionValue'],
                item['foodPortionUnit'],
                f"${item['price']:.2f}",
                put_buttons(['Add'], onclick=lambda _, i=item: handle_add(i))
            ]
            for item in matches
        ]
        put_table([headers] + rows)


def export_shopping_list():
    msg = export_csv(shoppingList)
    if msg.startswith("Error"):
        put_error(msg)
    else:
        put_success(msg)

def exit_app():
    msg = closeout(userPantry, shoppingList)
    if msg.startswith("Error"):
        put_error(msg)
    else:
        put_success(msg)


# === Dispatch Table ===

choice_handlers = {
    'View Pantry': render_pantry,
    'Edit Pantry Quantities': render_edit_pantry,
    'Add to Pantry': render_pantry_update,
    'Set Expiration Dates': render_set_exp,
    'View/Edit Item Thresholds': render_thresholds_update,
    'Get Nutrition': render_nutrition,
    'Lookup Price': render_price_lookup,
    'Add to Shopping List': render_add_to_shopping,
    'View Shopping List': render_shopping_list,
    'Edit Shopping List': render_edit_shopping_list,
    'Export Shopping List': export_shopping_list,
    'Expired Items': render_expired_items,
    'Exit': exit_app
}


def handle_choice(choice):
    handler = choice_handlers.get(choice)
    if handler:
        handler()
    else:
        put_error("Invalid menu option.", scope='main')


def pantry_main():
    put_buttons(list(choice_handlers.keys()), onclick=handle_choice)
    put_scope('main')  # output scope for all dynamic sections
    render_expired_items()


if __name__ == '__main__':
    start_server(pantry_main, port=8080, open_browser=True)
