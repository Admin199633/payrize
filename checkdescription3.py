
import json
import os
import requests

# Define the URL of the raw JSON files on GitHub
github_urls = [
    "https://raw.githubusercontent.com/Admin199633/payrize/main/Json_list/Home.json",
    "https://raw.githubusercontent.com/Admin199633/payrize/main/Json_list/Insurance.json",
    "https://raw.githubusercontent.com/Admin199633/payrize/main/Json_list/Leisure.json",
    "https://raw.githubusercontent.com/Admin199633/payrize/main/Json_list/Mortgage.json",
    "https://raw.githubusercontent.com/Admin199633/payrize/main/Json_list/Other.json",
    "https://raw.githubusercontent.com/Admin199633/payrize/main/Json_list/Transportation.json",
    "https://raw.githubusercontent.com/Admin199633/payrize/main/Json_list/Pharm.json"
    "https://raw.githubusercontent.com/Admin199633/payrize/main/Json_list/Business.json",

]

data = {}
for github_url in github_urls:
    # Make a GET request to fetch the raw JSON data
    response = requests.get(github_url)
    if response.status_code == 200:
        try:
            # Load JSON data from the response
            data[github_url] = response.json()
        except json.JSONDecodeError:
            print("Error decoding JSON for URL:", github_url)
    else:
        print("Failed to fetch JSON data from:", github_url)

# Create a set of existing descriptions for faster lookup
existing_descriptions = set()
for file_data in data.values():
    for expense in file_data:
        existing_descriptions.add(expense["Description"].lower())

# Load data from output.json
with open('output.json', 'r', encoding='utf-8') as output_file:
    output_data = json.load(output_file)

# Iterate through each entry in output.json
for entry in output_data:
    description = entry["Description"].lower()

    # Check if the description exists in any of the JSON files
    if description in existing_descriptions:
        # Iterate through each JSON file
        for github_url, file_data in data.items():
            for expense in file_data:
                if expense["Description"].lower() == description:
                    # Print the existing value
                    print("Existing value for", description, "in", os.path.basename(github_url), ":", expense["Amount"])
                    # Check if Flag already exists, if not add it
                    if "Flag" not in entry:
                        entry["Flag"] = []
                    # Add the flag to the entry in output.json
                    entry["Flag"].append(os.path.basename(github_url).split('.')[0])
                    break
    else:
        # If no match found, mark Flag as "None"
        entry["Flag"] = "None"

# Capitalize the first letter of the Description if an exact match is found
for entry in output_data:
    description = entry["Description"].lower()
    if entry["Flag"] != "None" and description in existing_descriptions:
        entry["Description"] = description.capitalize()

# Write the updated data back to output.json
with open('output2.json', 'w', encoding='utf-8') as output_file:
    json.dump(output_data, output_file, ensure_ascii=False, indent=4)
