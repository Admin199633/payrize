import json

# Load JSON data from input file
with open("output4.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# Function to filter out lines containing keys starting with "Unnamed"
def filter_unnamed(obj):
    return {key: value for key, value in obj.items() if not key.startswith("Unnamed")}

# Filter out lines containing keys starting with "Unnamed"
filtered_data = [filter_unnamed(obj) for obj in data]

# Save filtered JSON data to output file
with open("output5.json", "w", encoding="utf-8") as output_file:
    json.dump(filtered_data, output_file, ensure_ascii=False, indent=4)

print("Filtered JSON data saved to 'output5.json'.")
