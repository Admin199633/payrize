import json

# Load data from output3.json
with open('output3.json', 'r', encoding='utf-8') as output_file:
    output_data = json.load(output_file)

# Define the list of categories
categories = [
    "Home",
    "Leisure",
    "Transportation",
    "Insurance",
    "Pharm",
    "Business",
    "Mortgage",
    "Other"
]

# Iterate through each object in output3.json
for obj in output_data:
    # Check if the "Flag" field contains multiple values
    if isinstance(obj["Flag"], list) and len(obj["Flag"]) > 1:
        print("Multiple values found in 'Flag' field for description:", obj["Description"])
        print("Current values:", obj["Flag"])

        # Prompt the user to choose a category
        print("Choose a category to keep:")
        for index, category in enumerate(categories, start=1):
            print(f"{index}: {category}")

        # Validate the user's input
        while True:
            choice = input("Enter the number corresponding to the category: ")
            if choice.isdigit() and 1 <= int(choice) <= len(categories):
                chosen_category = categories[int(choice) - 1]
                obj["Flag"] = [chosen_category]
                break
            else:
                print("Invalid input. Please enter a number from 1 to", len(categories))

# Write the updated data back to output3.json
with open('output4.json', 'w', encoding='utf-8') as output_file:
    json.dump(output_data, output_file, ensure_ascii=False, indent=4)

print("Values in 'Flag' field have been modified in output4.json.")
