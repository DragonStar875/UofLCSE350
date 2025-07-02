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

filtered_data = []

for food in foods:
    entry = {"description": food.get("description", "Unknown")}

    for nutrient in food.get("foodNutrients", []):
        name = nutrient.get("nutrient", {}).get("name")
        if name in target_nutrients:
            amount = nutrient.get("amount")
            unit = nutrient.get("nutrient", {}).get("unitName", "")
            entry[name] = f"{amount} {unit}" if amount is not None else "N/A"

    if any(n in entry for n in target_nutrients):
        filtered_data.append(entry)

# Output to JSON
with open("usda_filtered_foods.json", "w") as jf:
    json.dump(filtered_data, jf, indent=2)

# Output to CSV
csv_headers = ["description"] + list(target_nutrients)
with open("usda_filtered_foods.csv", "w", newline='') as cf:
    writer = csv.DictWriter(cf, fieldnames=csv_headers)
    writer.writeheader()
    for row in filtered_data:
        writer.writerow(row)
