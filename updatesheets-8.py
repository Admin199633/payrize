import os.path
import json
import time
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scopes and spreadsheet ID
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
SPREADSHEET_ID = "1ncWrIEXjrAjC4h_hwBgzWNQvig-1ZAjF7F7k5-fxfS0"
CLIENT_SECRETS_FILE = "C:\\Users\\LS\\Downloads\\credentials.json" # Replace with the path to your JSON file
REQUEST_DELAY = 2  # Delay between requests in seconds

def find_next_empty_row(sheet, flag_column):
    """
    Find the next empty row in the specified column.
    """
    range_ = f"{flag_column}2:{flag_column}"  # Start from the second row
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range_
    ).execute()
    values = result.get('values', [])

    if not values:
        return 2  # If the column is completely empty, return the second row
    else:
        return len(values) + 2  # Return the next empty row

def main():
    """Post JSON data to a Google Sheets document."""
    creds = None
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES
    )
    creds = flow.run_local_server(port=0)

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        # Define the range A1:Z1
        range_ = "A7:Z7"

        # Get the values from the specified range
        print("Getting values from spreadsheet...")
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_
        ).execute()

        # Extract the values
        values = result.get("values", [])

        # Check if there are any values
        if not values:
            print("No data found.")
        else:
            # Iterate over each cell in the first row (columns A-Z)
            for i, column in enumerate(values[0]):
                flag_column = chr(65 + i)  # Column letter (A-Z)
                flag = column.strip()  # Remove any leading/trailing whitespaces

                # Find the next empty row in the column
                next_row = find_next_empty_row(sheet, flag_column)

                # Iterate over each entry in json_data
                for entry in json_data:
                    entry_flags = entry.get('Flag', [])
                    if flag in entry_flags:
                        description = entry.get('Description', '')
                        amount = entry.get('Amount', '')  # New line to get the amount
                        date_timestamp = entry.get('Date', '')  # New line to get the date

                        # Convert timestamp to datetime object
                        date = datetime.fromtimestamp(date_timestamp / 1000.0).strftime('%Y-%m-%d')

                        # Write the data to the next empty row
                        body = {
                            'values': [[description, amount, date]]
                        }
                        update_range = f"{flag_column}{next_row}:{chr(65 + i + 2)}{next_row}"  # Dynamically calculate the last column
                        request = sheet.values().update(
                            spreadsheetId=SPREADSHEET_ID,
                            range=update_range,
                            valueInputOption='RAW',
                            body=body
                        )
                        response = request.execute()

                        print(f"Wrote description '{description}', amount '{amount}', and date '{date}' to the sheet.")

                        # Increment next_row for the next entry
                        next_row += 1

                        # Add a delay between requests to avoid exceeding quota
                        print(f"Waiting for {REQUEST_DELAY} seconds before the next request...")
                        time.sleep(REQUEST_DELAY)

        print("Data successfully written to the sheet.")

    except HttpError as error:
        print(f"An HTTP error {error.resp.status} occurred:\n{error._get_reason()}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Read the JSON file
    with open("output5.json", "r",
              encoding="utf-8") as json_file:
        json_data = json.load(json_file)
    main()
