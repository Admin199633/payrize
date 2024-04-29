import os
import json


def load_json_files():
    json_files = [filename for filename in os.listdir() if filename.endswith('.json')]
    data = {}
    for file_name in json_files:
        with open(file_name, 'r', encoding='utf-8') as file:
            data[file_name] = json.load(file)
    return data


def get_existing_descriptions(data):
    existing_descriptions = set()
    for file_data in data.values():
        for expense in file_data:
            existing_descriptions.add(expense["Description"].lower())
    return existing_descriptions


def assign_flag(entry, categories):
    choice = input(
        "Please choose a category to assign (1: Home, 2: Leisure, 3: Transportation, 4: Insurance, 5: Pharm, 6: Business, 7: Mortgage, 8: Other): ")
    if choice.isdigit() and 1 <= int(choice) <= 8:
        category_index = int(choice) - 1
        flag = categories[category_index]
        entry["Flag"] = [flag] if isinstance(entry["Flag"], str) else entry["Flag"] + [flag]
    else:
        print("Invalid choice! Flag remains unchanged.")


def process_output(output_data, data, existing_descriptions, categories):
    for entry in output_data:
        description = entry["Description"].lower()
        if description in existing_descriptions:
            for expense in data['output2.json']:
                if expense["Description"].lower() == description:
                    print("Existing value for", description, "in output2.json:", expense["Amount"])
                    if entry["Flag"] == "None":
                        print("The Flag value is 'None' for the entry:", description)
                        assign_flag(entry, categories)
                    break
        else:
            entry["Flag"] = None


def main():
    data = load_json_files()
    existing_descriptions = get_existing_descriptions(data)

    with open('output2.json', 'r', encoding='utf-8') as output_file:
        output_data = json.load(output_file)

    categories = ["Home", "Leisure", "Transportation", "Insurance", "Pharm", "Business", "Mortgage", "Other"]

    process_output(output_data, data, existing_descriptions, categories)

    for entry in output_data:
        description = entry["Description"].lower()
        if entry["Flag"] is not None and description in existing_descriptions:
            entry["Description"] = description.capitalize()

    with open('output3.json', 'w', encoding='utf-8') as output_file:
        json.dump(output_data, output_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
