import pandas as pd

userPantry = pd.read_csv('userPantry.csv')

def add_to_userPantry(userPantry, food_name, quantity):
    try:

        # Preliminary checks
        if userPantry.isEmpty:
            return f'Failed to gather userPantry.csv, check for path or missing data error.'
        if food_name not in userPantry['food_name']:
            return f'Item not found, check your spelling. You entered: {food_name}.'
        if not isinstance(quantity, int):
            return f'The quantity you select must be an integer. You entered: {quantity}'

        # Function processes
        current = userPantry.loc[userPantry['food_name'] == food_name, 'qty']

        if current + quantity < 0:
            return f'Inventory amount for {food_name} must be greater than or equal to zero.'


        # Output
        userPantry.loc[userPantry['food_name'] == food_name, 'qty'] += quantity
        return f'Inventory amount for {food_name} changed from {current} to {current + quantity}.'

    except Exception as e:
        return f'Something went wrong during the modification of the userPantry: {e}'

