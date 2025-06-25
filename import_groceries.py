import pandas as pd
def import_groceries():
    allGroceries = pd.read_csv('allGroceries.csv')
    return allGroceries