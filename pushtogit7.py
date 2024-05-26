import json
import requests
import base64

def decode_hebrew(text):
    return text.encode('utf-8').decode('unicode-escape')

def encode_hebrew(text):
    return text.encode('utf-8').decode()

def entry_exists(existing_data, new_description):
    for entry in existing_data:
        if entry.get("Description") == new_description:
            return True
    return False

def push_to_github(file_name, data):
    try:
        # Personal access token for authentication
        access_token = "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"

        # Specify repository and file path
        repo = "Admin199633/payrize"
        file_path = f"Json_list/{file_name}.json"  # Assuming JSON files are stored in a folder named "Json_list"

        # Construct the API URL
        url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
        print("Trying to push data to file:", file_path)  # Print the full file path
        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Retrieve existing file contents from GitHub
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse existing data from the response
        existing_data = json.loads(base64.b64decode(response.json().get('content', '')).decode('utf-8'))

        # Filter out entries that already exist in the file
        new_entries = [entry for entry in data if not entry_exists(existing_data, decode_hebrew(entry.get("Description", "")))]

        if new_entries:
            # Append new unique data to the existing JSON file
            existing_data.extend(new_entries)

            # Convert the updated data back to JSON format
            updated_content = json.dumps(existing_data, indent=4, ensure_ascii=False)

            # Commit the changes to GitHub
            payload = {
                "message": "Updated data",
                "content": base64.b64encode(updated_content.encode()).decode(),
                "sha": response.json().get('sha', '')
            }
            response = requests.put(url, headers=headers, json=payload)
            response.raise_for_status()
            return len(new_entries)  # Return the number of unique objects inserted
        else:
            return 0  # No new unique data to insert
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
