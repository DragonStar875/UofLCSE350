import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import pytest
from source_functions.shoppingList import addItem, removeItem

@pytest.fixture
def shopping_csv(tmp_path):
    # Define the path for the sourceCSV directory and the CSV file
    source_csv_dir = tmp_path / "sourceCSV"
    shopping_list_file = source_csv_dir / "shoppingList_test_data.csv"

    # Create the sourceCSV directory if it doesn't exist
    source_csv_dir.mkdir(parents=True, exist_ok=True)

    # Define the data to be written to the CSV file
    data = [
        ["item_name", "price"],
        ["bananas", 1.54],
        ["tomatoes", 1.82],
        ["ground beef", 5.64],
        ["milk", 2.79],
        ["eggs", 3.25],
        ["bread", 2.5],
        ["cheddar cheese", 4.1],
        ["yogurt", 1.25],
        ["spinach", 2.2],
        ["apple", 0.99],
        ["carrot", 1.05],
        ["chicken breast", 6.45],
        ["tofu", 2.35],
        ["black beans", 1],
        ["lentils", 1.2],
        ["rice", 2.4],
        ["pasta", 1.5],
        ["broccoli", 2],
        ["cauliflower", 2.35],
        ["potatoes", 3],
        ["onions", 1.3],
        ["garlic", 0.7],
        ["olive oil", 6.99],
        ["butter", 4.75],
        ["cream", 3.4],
        ["orange juice", 3.25],
        ["strawberries", 3.99],
        ["blueberries", 4.1],
        ["zucchini", 1.8],
        ["cucumber", 1.55]
    ]

    # Write the data to the CSV file
    df = pd.DataFrame(data[1:], columns=data[0])
    df.to_csv(shopping_list_file, index=False)

    # Return the path to the CSV file for use in tests
    return shopping_list_file


def test_csv_loads_correctly(shopping_csv):
    # Convert the CSV file to a pandas DataFrame
    df = pd.read_csv(shopping_csv)

    # make sure the list is not empty
    assert not df.empty, "The shopping list CSV file is empty."

    # check that the df contains the expected number of rows
    assert len(df) == 30, f"Expected 30 rows, but got {len(df)}."

    # make sure first row is correct
    assert df.iloc[0]['item_name'] == 'bananas', "First item is not 'bananas'."
    assert df.iloc[0]['price'] == 1.54, "Price of 'bananas' is not 1.54."

    # also check last row
    assert df.iloc[-1]['item_name'] == 'cucumber', "Last item is not 'cucumber'."
    assert df.iloc[-1]['price'] == 1.55, "Price of 'cucumber' is not 1.55."

def test_add_item(shopping_csv):
    new_item_name = "avocado"
    new_price = 2.99

    # call the function
    addItem(str(shopping_csv), new_item_name, new_price)

    # Ensure that the name "avocado" exists in the item_names
    df = pd.read_csv(shopping_csv)
    assert new_item_name in df["item_name"].values, "Item was not added."
    assert float(df[df["item_name"] == new_item_name]["price"]) == new_price

def test_remove_item(shopping_csv):
    item_to_remove = "milk"

    #Checks if item exists in inventory before removing
    df_before = pd.read_csv(shopping_csv)
    assert item_to_remove in df_before["item_name"].values

    # tests the function
    removeItem(str(shopping_csv), item_to_remove)

    # Ensure the row is deleted
    df_after = pd.read_csv(shopping_csv)
    assert item_to_remove not in df_after["item_name"].values, "Item was not removed."
    assert len(df_after) == len(df_before) - 1