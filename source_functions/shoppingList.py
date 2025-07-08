import csv

import pandas as pd


# userPantry = pd.read_csv('userPantry.csv')
# shoppingList = pd.read_csv('shoppingList.csv')
# allGroceries = pd.read_csv('scraper/allGroceries.csv')

def addItem(shoppingList, item_name, price, quantity):
    with open(shoppingList, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([item_name, price, quantity])

def removeItem(filename, item_name, quantity_to_remove):
    updated_rows = []
    item_found = False

    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)

        for row in reader:
            if row[0] == item_name:
                item_found = True
                current_quantity = int(row[2])
                new_quantity = current_quantity - quantity_to_remove

                # Only keep the row if new quantity > 0
                if new_quantity > 0:
                    row[2] = str(new_quantity)
                    updated_rows.append(row)
                # else, the item is removed by not appending
            else:
                updated_rows.append(row)

    # Write back the updated content
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(updated_rows)

    if not item_found:
        raise ValueError(f"Item '{item_name}' not found in the shopping list.")