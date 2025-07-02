import json
import csv

# Load structured USDA JSON
with open("FoodData_Central_foundation_food_json_2025-04-24.json", "r") as f:
    data = json.load(f)

# Extract top-level list of foods
foods = data.get("FoundationFoods", [])
if not isinstance(foods, list):
    raise ValueError("Expected 'FoundationFoods' to be a list.")

# Nutrients of interest
target_nutrients = {
    "Protein",
    "Carbohydrate, by difference",
    "Total lipid (fat)"
}

price_by_category = {
    "Vegetables and Vegetable Products": 0.40,
    "Fruits and Fruit Juices": 0.55,
    "Legumes and Legume Products": 0.50,
    "Dairy and Egg Products": 1.20,
    "Cereal Grains and Pasta": 0.35,
    "Nut and Seed Products": 1.80,
    "Fats and Oils": 0.85,
    "Baked Products": 1.10,
    "Beef Products": 2.50,
    "Pork Products": 2.20,
    "Poultry Products": 1.90,
    "Finfish and Shellfish Products": 3.00,
    "Sweets": 1.30,
    "Spices and Herbs": 3.50,
    "Soups, Sauces, and Gravies": 1.00,
    "Restaurant Foods": 2.80,
    "Lamb, Veal, and Game Products": 3.20,
    "Beverages": 0.75
}

filtered_data = []

for food in foods:
    entry = {
        "description": food.get("description", "Unknown"),
        "category": None,
        "foodPortionValue": "N/A",
        "foodPortionUnit": "N/A"
    }

    # Extract nutrient values
    for nutrient in food.get("foodNutrients", []):
        name = nutrient.get("nutrient", {}).get("name")
        if name in target_nutrients:
            amount = nutrient.get("amount")
            unit = nutrient.get("nutrient", {}).get("unitName", "")
            entry[name] = f"{amount} {unit}" if amount is not None else "N/A"

    # Handle foodPortions gracefully
    # Handle foodPortions gracefully or default to 100g
    portions = food.get("foodPortions", [])
    if portions:
        first_portion = portions[0]
        value = first_portion.get("value")
        unit = first_portion.get("measureUnit", {}).get("abbreviation")

        entry["foodPortionValue"] = value if value is not None else first_portion.get("gramWeight", 100)
        entry["foodPortionUnit"] = unit if unit else "g"
    else:
        entry["foodPortionValue"] = 100
        entry["foodPortionUnit"] = "g"


    # Extract category from inputFoods[3] if available
    try:
        input_foods = food.get("inputFoods", [])
        if len(input_foods) > 3:
            category_desc = input_foods[3]["inputFood"]["foodCategory"]["description"]
            entry["category"] = category_desc
            entry["price"] = price_by_category.get(category_desc, None)
    except (KeyError, TypeError, IndexError):
        pass


    # Save entry if it has any target nutrient
    if any(n in entry for n in target_nutrients):
        filtered_data.append(entry)

# Output to JSON
with open("usda_filtered_foods.json", "w") as jf:
    json.dump(filtered_data, jf, indent=2)

# Output to CSV
csv_headers = ["description", "category", "foodPortionValue", "foodPortionUnit", "price"] + list(target_nutrients)
with open("usda_filtered_foods.csv", "w", newline='') as cf:
    writer = csv.DictWriter(cf, fieldnames=csv_headers)
    writer.writeheader()
    for row in filtered_data:
        writer.writerow({key: row.get(key, "") for key in csv_headers})
