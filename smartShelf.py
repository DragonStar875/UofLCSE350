import pandas as pd

#import userPantry
userPantry = pd.read_csv('userPantry.csv')

#import shoppingList
shoppingList = pd.read_csv('shoppingList.csv')

#import allGroceries
allGroceries = pd.read_csv('allGroceries.csv')

"""
set_threshold needs to edit items in userPantry such that the threshold


"""


def threshold_checker(userPantry):
    for row in userPantry.itertuples():
        #writing in pseudo before i forget
        #if item in userPantry qty on_hand < threshold, return item name.
        #consider an else that returns nothing if there's nothing < threshold
        if userPantry:
            print('meow')


def set_threshold(userPantry, food_name, threshold):
    return

def get_nutrition(userPantry, food_name):
    return userPantry.loc[userPantry['item_name'] == food_name, ['protein', 'fat', 'calories', 'carbohydrates', 'sugar']]


def get_price(allGroceries, food_name):
    return allGroceries.loc[allGroceries['item_name' == food_name, ['food_name','quantity', 'price']]]

def get_shoppingList(shoppingList):
    return shoppingList


#update shoppingList needs to write new item(s0 to shopingList dataframe
def update_shoppingList(shoppingList, food_name):
    return shoppingList

def get_userPantry(userPantry):
    return userPantry



#closeout must save any changes made to userPantry and shoppingList
def closeout(userPantry, shoppingList):
    exit()