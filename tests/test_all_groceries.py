import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import pytest

@pytest.fixture
def allGroceries_csv(tmp_path):
    # Define the path for the sourceCSV directory and the CSV file
    source_csv_dir = tmp_path / "sourceCSV"
    all_groceries_file = source_csv_dir / "allGroceries.csv"

    # Create the sourceCSV directory if it doesn't exist
    source_csv_dir.mkdir(parents=True, exist_ok=True)

    # Define the data to be written to the CSV file
    data = [
        ["description","category","foodPortionValue","foodPortionUnit","price","Carbohydrate, by difference","Protein","Total lipid (fat)","Calories"],
        ["Hummus, commercial","Legumes and Legume Products",2,"tbsp",0.5,14.9,7.35,17.1,242.9],
        ["Tomatoes, grape, raw","Vegetables and Vegetable Products",5,"tomatoes",0.4,5.51,0.83,0.63,31.03],
        ["Beans, snap, green, canned, regular pack, drained solids","Vegetables and Vegetable Products",1,"cup",0.4,4.11,1.04,0.39,24.11],
        ["Frankfurter, beef, unheated","Sausages and Luncheon Meats",1,"piece",2.39,2.89,11.7,28,310.36],
        ["Nuts, almonds, dry roasted, with salt added","Nut and Seed Products",1,"cup",1.8,16.2,20.4,57.8,666.6],
        ["Kale, raw","Vegetables and Vegetable Products",1,"cup",0.4,4.42,2.92,1.49,42.77],
        ["Egg, whole, raw, frozen, pasteurized","Dairy and Egg Products",1,"oz",1.2,0.91,12.3,10.3,145.54],
        ["Egg, white, raw, frozen, pasteurized","Dairy and Egg Products",1,"oz",1.2,0.74,10.1,0.16,44.8],
        ["Egg, white, dried","Dairy and Egg Products",1,"tbsp",1.2,6.02,79.9,0.65,349.53],
        ["Onion rings, breaded, par fried, frozen, prepared, heated in oven","Vegetables and Vegetable Products",1,"piece",0.4,36.3,4.52,14.4,292.88]
        
    ]

    # Write the data to the CSV file
    df = pd.DataFrame(data[1:], columns=data[0])
    df.to_csv(all_groceries_file, index=False)

    # Return the path to the CSV file for use in tests
    return all_groceries_file


def test_csv_loads_correctly(allGroceries_csv):
    # Convert the CSV file to a pandas DataFrame
    df = pd.read_csv(allGroceries_csv)

    # make sure the list is not empty
    assert not df.empty, "The shopping list CSV file is empty."

    # check that the df contains the expected number of rows
    assert len(df) == 10, f"Expected 10 rows, but got {len(df)}."

    # make sure first row is correct
    assert df.iloc[0]['description'] == 'Hummus, commercial', "First item is not 'Hummus, commercial'."
    assert df.iloc[0]['category'] == "Legumes and Legume Products", "Category of 'Hummus, commercial' is not 'Legumes and Legume Products'."
    assert df.iloc[0]['foodPortionValue'] == 2, "foodPortionValue of 'Hummus, commercial' is not 2."
    assert df.iloc[0]['foodPortionUnit'] == "tbsp", "foodPortionUnit of 'Hummus, commercial' is not 'tbsp'."
    assert df.iloc[0]['price'] == 0.5, "price of 'Hummus, commercial' is not 0.5."
    assert df.iloc[0]['Carbohydrate, by difference'] == 14.9, "Carbohydrate, by difference of 'Hummus, commercial' is not 14.9."
    assert df.iloc[0]['Protein'] == 7.35, "Protein of 'Hummus, commercial' is not 7.35."
    assert df.iloc[0]['Total lipid (fat)'] == 17.1, "Total lipid (fat) of 'Hummus, commercial' is not 17.1."
    assert df.iloc[0]['Calories'] == 242.9, "Calories of 'Hummus, commercial' is not 242.9."

    # also check last row
    assert df.iloc[-1]['description'] == 'Onion rings, breaded, par fried, frozen, prepared, heated in oven', "Last item is not 'Hummus, commercial'."
    assert df.iloc[-1]['category'] == "Vegetables and Vegetable Products", "Category of 'Onion rings, breaded, par fried, frozen, prepared, heated in oven' is not 'Vegetables and Vegetable Products'."
    assert df.iloc[-1]['foodPortionValue'] == 1, "foodPortionValue of 'Onion rings, breaded, par fried, frozen, prepared, heated in oven' is not 1."
    assert df.iloc[-1]['foodPortionUnit'] == "piece", "foodPortionUnit of 'Onion rings, breaded, par fried, frozen, prepared, heated in oven' is not 'piece'."
    assert df.iloc[-1]['price'] == 0.4, "price of 'Onion rings, breaded, par fried, frozen, prepared, heated in oven' is not 0.4."
    assert df.iloc[-1]['Carbohydrate, by difference'] == 36.3, "Carbohydrate, by difference of 'Onion rings, breaded, par fried, frozen, prepared, heated in oven' is not 36.3."
    assert df.iloc[-1]['Protein'] == 4.52, "Protein of 'Onion rings, breaded, par fried, frozen, prepared, heated in oven' is not 4.52."
    assert df.iloc[-1]['Total lipid (fat)'] == 14.4, "Total lipid (fat) of 'Onion rings, breaded, par fried, frozen, prepared, heated in oven' is not 14.4."
    assert df.iloc[-1]['Calories'] == 292.88, "Calories of 'Onion rings, breaded, par fried, frozen, prepared, heated in oven' is not 292.88."