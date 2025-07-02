import pandas as pd
from pywebio.output import put_tabs, put_table, put_buttons, popup, put_scope, clear_scope
import time
from shoppingList import addItem


def grocery_options(shopping_list_csv, item, price):
    popup(f"Actions for {item}", [
        put_buttons(
            ['Add to Shopping List'],
            onclick=[lambda: addItem(shopping_list_csv, item, price)]
        )
    ])


def render_shopping_list():
    df = pd.read_csv("../shoppingList.csv")
    shopping_table = [df.columns.tolist()] + df.values.tolist()
    clear_scope('shopping_tab')
    put_table(shopping_table, scope='shopping_tab')


def main():
    shopping_list_csv = "../shoppingList.csv"

    df = pd.read_csv("../scraper/allGroceries.csv")
    df.columns = df.columns.str.strip()

    header = df.columns.tolist()
    header.append('')
    grocery_table = [header]

    for _, row in df.iterrows():
        row_data = row.tolist()
        item_val = row[header[0]]
        price_val = row[header[3]]

        menu_button = put_buttons(
            ['⋮'],
            onclick=[lambda i=item_val, p=price_val: grocery_options(shopping_list_csv, i, p)]
        )

        row_data.append(menu_button)
        grocery_table.append(row_data)

    put_tabs([
        {'title': 'Grocery List', 'content': [put_table(grocery_table)]},
        {'title': 'Shopping List', 'content': [put_scope('shopping_tab')]}
    ])

    while True:
        render_shopping_list()
        time.sleep(10)


if __name__ == '__main__':
    from pywebio.platform.tornado_http import start_server

    start_server(main, port=8080)
