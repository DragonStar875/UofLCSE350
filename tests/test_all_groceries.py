import os
import pandas as pd

def test_allGroceries_csv_structure_and_types():
    # Step 1: Construct path to allGroceries.csv (one level up from tests/)
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'allGroceries.csv'))

    # Step 2: Ensure file exists
    assert os.path.isfile(file_path), f"File not found: {file_path}"

    # Step 3: Load CSV
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        assert False, f"Failed to load CSV: {e}"

    # Step 4: Check expected columns
    expected_columns = [
        'description', 'category', 'foodPortionValue', 'foodPortionUnit',
        'price', 'Carbohydrate, by difference', 'Protein',
        'Total lipid (fat)', 'Calories'
    ]
    assert list(df.columns) == expected_columns, \
        f"Unexpected columns: {list(df.columns)}\nExpected: {expected_columns}"
