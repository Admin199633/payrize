import pandas as pd
ame_xl= input("Please enter name XL: ")
name_xl="Export_8_04_2024.xlsx"
path = 'C:\\Users\\LS\\PycharmProjects\\rizeup1\\modified_excel_file.xlsx'
# Load the Excel workbook

# טען את קובץ האקסל
df = pd.read_excel(path)
# המר את הנתונים לפורמט JSON ושימוש בעברית
json_data = df.to_json(orient='records', force_ascii=False)

# כתוב את הנתונים לקובץ JSON
with open('output.json', 'w', encoding='utf-8') as f:
    f.write(json_data)
