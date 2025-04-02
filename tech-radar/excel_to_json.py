import pandas as pd
import json 

# Define the filename
xlsx_filename = "radar_entries.xlsx"
json_filename = "config.json"

# Load the Excel file
xls = pd.ExcelFile(xlsx_filename)

# Extract the first sheet name (which is used as the date)
sheet_name = xls.sheet_names[0]

# Read the sheet
df = pd.read_excel(xlsx_filename, sheet_name=sheet_name)

# Convert DataFrame to JSON format expected by the website
json_data = {
    "date": sheet_name,
    "entries": df.where(pd.notna(df), "").to_dict(orient="records")  # Replace NaN with ""
}


# Save to JSON file
json_output_path = "config.json"
with open(json_output_path, "w") as json_file:
    json_file.write(json.dumps(json_data, indent=2))

# Provide download link
json_output_path
