import pandas as pd


userPantry = pd.read_csv('userPantry.csv')
"""
Incorporated into smartShelf.py
Function needs some kind of success/fail return value
and a try/catch block for critical_value, that determines if it is an int, non-negative, and not preposterously large 
"""
def set_critical(userPantry, food_name, critical_value):
    try:

        # Preliminary checks
        if userPantry.empty:
            return f'Failed to gather userPantry.csv, check for path or missing data error.'
        if not isinstance(critical_value, int):
            return "Error: Please ensure that your critical value is an integer."
        if food_name not in userPantry['item_name'].values:
            return "Item not found in pantry. Please check spelling."

        # Function processes
        if critical_value < 0:
            return "Error: Please ensure that your critical value is positive."
        if critical_value > 100:
            return "Error: Please ensure that your critical value is less than 100."


        userPantry.loc[userPantry['item_name'] == food_name, 'threshold'] = critical_value


        return f"Threshold for {food_name} was set to {critical_value}, checking critical values."

    except Exception as e:

        print(f"Something went wrong during the critical value setting process: {e}")
        return e
