import pandas as pd

# Load the Excel workbook
df = pd.read_excel("modified_excel_file.xlsx")

# Convert the data to JSON format, using Hebrew
json_data = df.to_json(orient='records', force_ascii=False)

# Write the data to a JSON file
with open('output.json', 'w', encoding='utf-8') as f:
    f.write(json_data)
