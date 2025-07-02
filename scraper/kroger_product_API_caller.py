import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
import json


# 🔐 Fill these in with your Kroger Developer credentials
CLIENT_ID = 'smartshelf-grocerygetter-bbc6kgtg'
CLIENT_SECRET = 'AwnDhIJKlLyw2DEOmj6khqmBsnOo0rARNSWPpExD'


# Step 1: Get access token
def get_access_token():
    url = "https://api-ce.kroger.com/v1/connect/oauth2/token"  # Updated to Certification environment
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "scope": "product.compact"
    }

    response = requests.post(url, headers=headers, data=data,
                             auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get token: {response.status_code} {response.text}")

# Step 2: Search for a product
def search_products(query, token, location_id=None, limit=5):
    url = "https://api-ce.kroger.com/v1/products"  # Updated to Certification environment
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    params = {
        "filter.term": query,
        "filter.limit": limit
    }
    if location_id:
        params["filter.locationId"] = location_id

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Product search failed: {response.status_code} {response.text}")

# Step 3: Parse product data into structured format
def extract_grocery_data(products):
    rows = []
    for product in products.get("data", []):
        desc = product.get("description", "")
        brand = product.get("brand", "")
        product_id = product.get("productId", "")
        product_url = f"https://www.kroger.com/p/{desc.replace(' ', '-').lower()}/{product_id}" if product_id else ""

        for item in product.get("items", []):
            size = item.get("size", "")
            price = item.get("price", {}).get("regular", "")
            nutrition = {fact['name'].lower(): fact['amount'] for fact in item.get("nutritionalInformation", [])}
            print("=== Raw Item ===")
            print(f"  Description: {desc}")
            print(f"  Size: {size}")
            print("  Item Keys:", list(item.keys()))
            print("  Price:", item.get("price"))
            print("  Nutrition Info:", item.get("nutritionalInformation"))
            print()

            rows.append({
                "item_name": desc,
                "brand": brand,
                "size": size,
                "price": price,
                "calories": nutrition.get("calories", ""),
                "carbohydrates": nutrition.get("total carbohydrate", ""),
                "sugar": nutrition.get("sugars", ""),
                "protein": nutrition.get("protein", ""),
                "fat": nutrition.get("total fat", ""),
                "url": product_url
            })
    return rows

# Step 4: Query several items and build the CSV
def build_all_groceries_csv():
    token = get_access_token()
    search_terms = ["milk", "bread", "apple juice", "eggs", "chicken", "beef","beans","rice","corn","flour"]
    all_rows = []
    for term in search_terms:
        print(f"Searching for {term}...")
        products = search_products(term, token)
        rows = extract_grocery_data(products)
        all_rows.extend(rows)

    df = pd.DataFrame(all_rows)
    df.to_csv("kroger_API_results.csv", index=False)
    print("Saved kroger_API_results.csv with", len(df), "items.")

if __name__ == '__main__':
    build_all_groceries_csv()
