import pandas as pd
path= "C:\\Users\\LS\\PycharmProjects\\pythonProject5\\"
# טען את קובץ האקסל
df = pd.read_excel('modified_excel_file.xlsx')
# המר את הנתונים לפורמט JSON ושימוש בעברית
json_data = df.to_json(orient='records', force_ascii=False)

# כתוב את הנתונים לקובץ JSON
with open('output.json', 'w', encoding='utf-8') as f:
    f.write(json_data)
