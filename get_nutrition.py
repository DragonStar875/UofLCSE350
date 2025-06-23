import pandas as pd


userPantry = pd.read_csv('userPantry.csv')

def get_nutrition(userPantry, food_name):
    return userPantry.loc[userPantry['item_name'] == food_name ['food_name','protein', 'fat', 'calories', 'carbohydrates', 'sugar']]

