import json
import os
import requests

# Define the URL of the GitHub repository and the folder within it
repo_url = 'https://github.com/Admin199633/payrize/tree/main/Json%20list'

# Make a GET request to the repository URL
response = requests.get(repo_url)

# Check if the request was successful
if response.status_code == 200:
    # Extract the HTML content of the page
    html_content = response.text

    # Search for links to JSON files in the HTML content
    json_urls = []
    start_index = 0
    while True:
        # Find the start index of the next link
        start_index = html_content.find('href="', start_index)
        if start_index == -1:
            break  # No more links found

        # Find the end index of the link
        end_index = html_content.find('"', start_index + 6)
        if end_index == -1:
            break  # Malformed link

        # Extract the URL and append it to the list
        link = html_content[start_index + 6:end_index]
        if link.endswith('.json'):
            json_urls.append(link)

        # Move to the next position
        start_index = end_index

    # Download JSON files from the URLs
    for json_url in json_urls:
        # Construct the full URL of the JSON file
        full_url = f'https://raw.githubusercontent.com/Admin199633/payrize/main/{json_url}'

        # Get the filename from the URL
        filename = os.path.basename(json_url)

        # Download the JSON file
        response = requests.get(full_url)
        if response.status_code == 200:
            # Save the content to a file
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {filename}")
else:
    print("Failed to fetch repository content")

# Define the list of JSON files with their filenames
json_files = [filename for filename in os.listdir() if filename.endswith('.json')]

data = {}

for file_name in json_files:
    with open(file_name, 'rb') as file:
        try:
            data[file_name] = json.load(file)
        except UnicodeDecodeError:
            # Try reading the file with a different encoding
            with open(file_name, 'r', encoding='cp1255') as alt_file:
                data[file_name] = json.load(alt_file)

# Create a set of existing descriptions for faster lookup
existing_descriptions = set()
for file_name, file_data in data.items():
    for expense in file_data:
        existing_descriptions.add(expense["Description"].lower())

# Load data from output.json
with open('output.json', 'r', encoding='utf-8') as output_file:
    output_data = json.load(output_file)

# Categories
categories = ["Home", "Leisure", "Transportation", "Insurance", "Pharm", "Business", "Mortgage", "Other"]

# Iterate through each entry in output.json
for entry in output_data:
    description = entry["Description"].lower()

    # Check if the description exists in any of the JSON files
    if description in existing_descriptions:
        # Iterate through each JSON file
        for file_name, file_data in data.items():
            for expense in file_data:
                if expense["Description"].lower() == description:
                    # Print the existing value
                    print("Existing value for", description, "in", os.path.basename(file_name), ":", expense["Amount"])
                    # Check if Flag is present in the entry and its value is null, if yes, prompt the user for input
                    if "Flag" not in entry or entry["Flag"] is None:
                        # Ask the user to choose a category to assign
                        print("The Flag value is 'None' for the entry:", description)
                        choice = input(
                            "Please choose a category to assign (1: Home, 2: Leisure, 3: Transportation, 4: Insurance, 5: Pharm, 6: Business, 7: Mortgage, 8: Other): ")
                        # Assign the chosen category to the Flag
                        if choice in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                            entry["Flag"] = categories[int(choice) - 1]
                        else:
                            print("Invalid choice! Flag remains 'None'.")
                    else:
                        # Convert Flag to list if it's a string
                        if isinstance(entry["Flag"], str):
                            entry["Flag"] = [entry["Flag"]]
                        # Add the flag to the entry in output.json
                        entry["Flag"].append(categories[int(choice) - 1])
                    break
    else:
        # If no match found, mark Flag as null
        entry["Flag"] = None

# Capitalize the first letter of the Description if an exact match is found
for entry in output_data:
    description = entry["Description"].lower()
    if entry["Flag"] is not None and description in existing_descriptions:
        entry["Description"] = description.capitalize()

# Write the updated data back to output.json
with open('output2.json', 'w', encoding='utf-8') as output_file:
    json.dump(output_data, output_file, ensure_ascii=False, indent=4)
