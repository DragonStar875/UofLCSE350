import csv

import pandas as pd


# userPantry = pd.read_csv('userPantry.csv')
# shoppingList = pd.read_csv('shoppingList.csv')
# allGroceries = pd.read_csv('scraper/allGroceries.csv')

def addItem(shoppingList, item_name, price):
    with open(shoppingList, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([item_name, price])

def removeItem(filename, item_name):
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = [row for row in reader if row[0] != item_name]

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)