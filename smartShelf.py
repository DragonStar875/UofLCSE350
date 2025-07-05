from pywebio.input import input, input_group, NUMBER
from pywebio.output import (
    put_text, put_table, put_success, put_error,
    put_buttons, put_scope, clear_scope, use_scope
)
from pywebio import start_server

from pantry_utils import (
    load_csvs, threshold_checker, get_nutrition, get_price,
    get_shopping_list, update_shopping_list,
    get_user_pantry, closeout
)

# === Load data ===
userPantry, shoppingList, allGroceries = load_csvs()

# === Section Handlers ===
#
# def render_pantry():
#     clear_scope('main')
#     data = get_user_pantry(userPantry)
#     put_table([list(data[0].keys())] + [list(d.values()) for d in data], scope='main')


# # def render_pantry():  ver 2
#     clear_scope('main')
#
#     data = get_user_pantry(userPantry)
#
#     # Step 1: Display Pantry Table
#     put_text("Current Pantry:", scope='main')
#     put_table([list(data[0].keys())] + [list(d.values()) for d in data], scope='main')
#
#     # Step 2: Create editable threshold form
#     inputs = []
#     for item in data:
#         inputs.append(
#             input(f"{item['item_name']} (current threshold: {item['threshold']})",
#                   name=item['item_name'], type=NUMBER, placeholder="Enter new threshold or leave blank")
#         )
#
#     form_data = input_group("Update Thresholds", inputs)
#
#     changes_made = False
#     for item in data:
#         val = form_data.get(item['item_name'])
#         if val != '' and val is not None:
#             try:
#                 threshold_val = int(val)
#                 if threshold_val < 0 or threshold_val > 1_000_000:
#                     put_error(f"Invalid threshold for {item['item_name']}: must be 0–1,000,000", scope='main')
#                 else:
#                     userPantry.loc[userPantry['item_name'] == item['item_name'], 'threshold'] = threshold_val
#                     changes_made = True
#             except ValueError:
#                 put_error(f"Invalid input for {item['item_name']}: must be an integer", scope='main')
#
#     if changes_made:
#         put_success("Thresholds updated.", scope='main')
#     else:
#         put_text("No thresholds were changed.", scope='main')

from pywebio.input import input_group, input, NUMBER
from pywebio.output import put_table, put_text, put_success, put_error, clear_scope

import re

def render_pantry():
    clear_scope('main')

    data = get_user_pantry(userPantry)

    put_text("Current Pantry:", scope='main')
    put_table([list(data[0].keys())] + [list(d.values()) for d in data], scope='main')

    # Create safe input names and build a mapping
    inputs = []
    name_map = {}

    for item in data:
        # Create a safe name: replace spaces and invalid chars
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
                if threshold_val < 0 or threshold_val > 1_000_000:
                    put_error(f"Invalid threshold for {original_name}: must be 0–1,000,000", scope='main')
                else:
                    userPantry.loc[userPantry['item_name'] == original_name, 'threshold'] = threshold_val
                    changes_made = True
            except ValueError:
                put_error(f"Invalid input for {original_name}: must be an integer", scope='main')

    if changes_made:
        put_success("Thresholds updated.", scope='main')
    else:
        put_text("No thresholds were changed.", scope='main')


def render_thresholds():
    clear_scope('main')
    low_items = threshold_checker(userPantry)
    if not low_items:
        put_success("All items are above threshold.", scope='main')
    else:
        put_table([list(low_items[0].keys())] + [list(d.values()) for d in low_items], scope='main')


"""
Nutrition lookups are working now!  Woohoo!  And it checks for df['description'].contains(food_name) so cheese returns a lot of rows :D"""
def render_nutrition():
    clear_scope('main')
    food = input("Enter item name to get nutrition:")
    result = get_nutrition(allGroceries, food)
    if not result:
        put_error("Item not found in groceries.", scope='main')
    elif isinstance(result, dict) and result.get("error"):
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

def exit_app():
    msg = closeout(userPantry, shoppingList)
    if msg.startswith("Error"):
        put_error(msg)
    else:
        put_success(msg)


# === Dispatch Table ===

choice_handlers = {
    'View Pantry': render_pantry,
    'Check Item Thresholds': render_thresholds,
    'Get Nutrition': render_nutrition,
    'Lookup Price': render_price_lookup,
    'Add to Shopping List': render_add_to_shopping,
    'View Shopping List': render_shopping_list,
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


if __name__ == '__main__':
    start_server(pantry_main, port=8080, open_browser=True)
