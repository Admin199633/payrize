import json
from github import Github
from github.GithubException import UnknownObjectException

# Custom encoding function to handle Hebrew characters
def hebrew_encoder(obj):
    if isinstance(obj, str):
        return obj.encode('unicode-escape').decode('utf-8')
    return obj

def entry_exists(existing_data, new_description):
    for entry in existing_data:
        if entry["Description"] == new_description:
            return True
    return False

def push_to_github(file_name, data):
    try:
        # Authenticate with GitHub using personal access token
        g = Github("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")

        # Specify repository and file path
        repo = g.get_repo("Admin199633/payrize")
        file_path = f"Json_list/{file_name}.json"  # Assuming JSON files are stored in a folder named "Json_list"

        # Convert data to JSON format with custom encoding
        json_data = json.dumps(data, default=hebrew_encoder, ensure_ascii=False, indent=4)

        # Retrieve existing file contents from GitHub
        try:
            contents = repo.get_contents(file_path)
            existing_data = json.loads(contents.decoded_content.decode('utf-8'))  # Decode the content

            # Filter out entries that already exist in the file
            new_entries = [entry for entry in data if not entry_exists(existing_data, entry["Description"])]

            if new_entries:
                # Append new unique data to the existing JSON file
                existing_data.extend(new_entries)

                # Convert the updated data back to JSON format with custom encoding
                updated_content = json.dumps(existing_data, default=hebrew_encoder, ensure_ascii=False, indent=4)

                # Commit the changes to GitHub
                repo.update_file(contents.path, "Updated data", updated_content, contents.sha)
                return len(new_entries)  # Return the number of unique objects inserted
            else:
                return 0  # No new unique data to insert
        except UnknownObjectException:
            # If the file does not exist, create a new file with the provided data
            repo.create_file(file_path, "Initial data", json_data.encode('utf-8'))
            return len(data)  # Return the number of objects inserted as all are unique
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0

def main():
    # Load data from the output file with UTF-8 encoding
    with open("output5.json", "r", encoding='utf-8') as file:
        data = json.load(file)
        print("Data loaded from output6.json:", data)

    total_inserted = 0
    # Iterate through the data and organize it based on the "Flag" value
    for entry in data:
        flag = entry.get("Flag", ["Other"])[0]  # Default to "Other" if no flag is provided
        print("Pushing entry to GitHub with flag:", flag)
        inserted_count = push_to_github(flag, [entry])  # Push the entry to the appropriate JSON file on GitHub
        total_inserted += inserted_count

    print(f"Total unique objects inserted: {total_inserted}")

if __name__ == "__main__":
    main()
