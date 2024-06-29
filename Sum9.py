import os.path
import json
import time
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scopes and spreadsheet ID
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
SPREADSHEET_ID = "1ncWrIEXjrAjC4h_hwBgzWNQvig-1ZAjF7F7k5-fxfS0"
CLIENT_SECRETS_FILE = "C:\\Users\\LS\\Downloads\\credentials.json"  # Replace with the path to your JSON file
REQUEST_DELAY = 2  # Delay between requests in seconds

def main():
    """Calculate the sum of the 'Price' columns in a Google Sheets document."""
    creds = None

    # Load credentials from file if exists
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            creds_data = json.load(token)
            creds = Credentials.from_authorized_user_info(creds_data)

    # If no valid credentials, initiate the OAuth flow
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        # Define the range A1:Z1 to get the headers
        range_ = "A7:Z7"

        # Get the values from the specified range
        print("Getting values from spreadsheet...")
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_
        ).execute()

        # Extract the headers
        headers = result.get("values", [])[0]

        # Initialize total sum accumulator
        total_price_sum = 0

        # Iterate over each header to find the "Price" columns
        for i, header in enumerate(headers):
            header_value = header.strip().upper()  # Normalize header value

            # Skip non-numeric headers
            if header_value != "PRICE":
                continue

            column_letter = chr(65 + i)  # Column letter (A-Z)
            price_range = f"{column_letter}2:{column_letter}"  # Range for the "Price" column

            # Get the values in the "Price" column
            print(f"Fetching values from range: {price_range}...")
            prices_result = sheet.values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=price_range
            ).execute()

            prices = prices_result.get('values', [])

            # Calculate the sum of the "Price" column
            total_sum = sum(float(price[0]) for price in prices if price and isinstance(price[0], str) and price[0].replace('.', '', 1).isdigit())

            # Print the total sum of the column
            print(f"Total sum of column '{header}' is: {total_sum}")

            # Add to the total price sum
            total_price_sum += total_sum

            # Print the formula used for calculation
            if len(prices) > 1:
                print(f"Formula used for calculation: {' + '.join(price[0] for price in prices if price and isinstance(price[0], str) and price[0].replace('.', '', 1).isdigit())}")

            # Write the total sum to the corresponding cell in row 2
            update_range = f"{column_letter}2"  # Cell to write the total sum in row 2
            body = {
                'values': [[total_sum]]
            }
            request = sheet.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=update_range,
                valueInputOption='RAW',
                body=body
            )
            response = request.execute()
            print(f"Total sum '{total_sum}' written to cell '{update_range}'.")

        # Print the total price sum of all "Price" columns
        print(f"\nTotal sum of all 'Price' columns: {total_price_sum}")

    except HttpError as error:
        print(f"An HTTP error {error.resp.status} occurred:\n{error._get_reason()}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Print the calculation method
    print("\nCalculation method: Summing up numeric values in the 'Price' columns.")

if __name__ == "__main__":
    main()
