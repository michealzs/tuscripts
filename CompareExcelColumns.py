import pandas as pd

# Load the two Excel files
file1_path = 'file1.xlsx'
file2_path = 'file2.xlsx'

# Load the second column from both files
column_name = 'Client Name'  # Replace with the actual column name
df1 = pd.read_excel(file1_path, sheet_name='Services Rendered Report Advanc', usecols=[1], names=[column_name])
df2 = pd.read_excel(file2_path, sheet_name='Services Rendered Report Advanc', usecols=[1], names=[column_name])

# Find the differences between the columns
differences = pd.concat([df1, df2]).drop_duplicates(keep=False)

# Output the differences
print("\n<==================>\n")
print("Differences in the second column:")
print("\n<==================>\n")
print(differences)
print("\n")
