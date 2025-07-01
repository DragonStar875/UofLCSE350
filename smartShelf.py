import pandas as pd

#import userPantry
userPantry = pd.read_csv('userPantry.csv')

#import shoppingList
shoppingList = pd.read_csv('shoppingList.csv')

#import allGroceries
allGroceries = pd.read_csv('allGroceries.csv')

"""
Considering a while loop for the main menu, such that application only terminates after selecting the option to exit and runs
closeout()
"""



def threshold_checker(userPantry):
    below_threshold = userPantry[userPantry['quantity'] < userPantry['critical_threshold']]
    if below_threshold.empty:
        return None
    return below_threshold[['item_name', 'quantity', 'critical_threshold']].to_dict('records')



"""
Function needs a try/catch for error handling if food_name not in userPantry 
food_name must be of type string, consider a toString function for all food_name cases
"""
def get_nutrition(userPantry, food_name):
    return userPantry.loc[userPantry['item_name'] == food_name, ['protein', 'fat', 'calories', 'carbohydrates', 'sugar']]



def get_price(allGroceries, food_name):
    result = allGroceries.loc[allGroceries['item_name'] == food_name, ['food_name','quantity', 'price']]
    if result.empty:
        return "Item cannot be found, please check your spelling"
    return result.to_dict('records')



"""
Needs some kind of formatting on the return value so it doesn't barf an ugly pandas dataFrame or a dictionary

"""
def get_shoppingList(shoppingList):
    return shoppingList.to_dict('records')
"""
update shoppingList needs to write new item(s) to shoppingList dataframe
consider **kwargs for multiple inputs
And should enumerate an additional column each time for rolling_total, as a sum of the price of each subsequent item
"""
def update_shoppingList(shoppingList, food_name):
    return shoppingList

"""
Function needs some kind of success/fail return value
and a try/catch block for critical_value, that determines if it is an int, non-negative, and not preposterously large 
"""
def set_critical(userPantry, food_name, critical_value):
    try:
        critical_value = int(critical_value)
        if critical_value < 0 or critical_value > 100:
            return "Error: Please ensure that your critical value is between 0 and 100"
        if food_name not in userPantry['item_name'].values:
            return "Item not found in pantry. Please check spelling."
        userPantry.loc[userPantry['item_name'] == food_name, 'critical_threshold'] = critical_value
        return f"Threshold for {food_name} set to {critical_value}."
    except ValueError:
        return "Critical value must be an integer."


"""
Needs some kind of formatting on the return value so it doesn't barf an ugly pandas dataFrame
"""
def get_userPantry(userPantry):
    return userPantry.to_dict('records')



"""
closeout must save any changes made to userPantry and shoppingList
minor error-handling here
"""
def closeout(userPantry, shoppingList):
    try:
        userPantry.to_csv("userPantry.csv", index=False)
        shoppingList.to_csv("shoppingList.csv", index=False)
        print("Changes successfully saved.")
    except Exception as e:
        print(f"Error saving data: {e}")
    exit()

