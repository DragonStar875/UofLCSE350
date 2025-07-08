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
        ["item_name", "price", "quantity"],
        ["bananas", 1.54, 1],
        ["tomatoes", 1.82, 1],
        ["ground beef", 5.64, 3],
        ["milk", 2.79, 2],
        ["eggs", 3.25, 23],
        ["bread", 2.5, 4],
        ["cheddar cheese", 4.1, 2],
        ["yogurt", 1.25, 42],
        ["spinach", 2.2, 1],
        ["apple", 0.99, 5],
        ["carrot", 1.05, 1],
        ["chicken breast", 6.45, 1],
        ["tofu", 2.35, 4],
        ["black beans", 1, 7],
        ["lentils", 1.2, 9],
        ["rice", 2.4, 6],
        ["pasta", 1.5, 2],
        ["broccoli", 2, 4],
        ["cauliflower", 2.35, 1],
        ["potatoes", 3, 1],
        ["onions", 1.3, 1],
        ["garlic", 0.7, 8],
        ["olive oil", 6.99, 2],
        ["butter", 4.75, 5],
        ["cream", 3.4, 10],
        ["orange juice", 3.25, 14],
        ["strawberries", 3.99, 11],
        ["blueberries", 4.1, 3],
        ["zucchini", 1.8, 2],
        ["cucumber", 1.55, 2]
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
    quantity = 4

    # call the function
    addItem(str(shopping_csv), new_item_name, new_price, quantity)

    # Ensure that the name "avocado" exists in the item_names
    df = pd.read_csv(shopping_csv)

    added_item = df[df["item_name"] == new_item_name]

    # Assertions
    assert not added_item.empty, "Item was not added."
    assert float(added_item["price"].iloc[0]) == new_price, "Price does not match."
    assert int(added_item["quantity"].iloc[0]) == quantity, "Quantity does not match."

def test_remove_item(shopping_csv):
    item_name = "yogurt"
    original_quantity = 42
    remove_quantity = 10

    # First, verify the item exists and has the expected quantity
    df = pd.read_csv(shopping_csv)
    assert item_name in df["item_name"].values, "Item does not exist initially."
    assert int(df[df["item_name"] == item_name]["quantity"].iloc[0]) == original_quantity, "Initial quantity mismatch."

    # Remove some quantity
    removeItem(str(shopping_csv), item_name, remove_quantity)

    # Reload and check updated quantity
    df = pd.read_csv(shopping_csv)
    updated_quantity = int(df[df["item_name"] == item_name]["quantity"].iloc[0])
    assert updated_quantity == original_quantity - remove_quantity, "Quantity not correctly reduced."

    # Remove the remaining quantity
    removeItem(str(shopping_csv), item_name, updated_quantity)

    df = pd.read_csv(shopping_csv)
    assert item_name not in df["item_name"].values, "Item should be completely removed but still exists."