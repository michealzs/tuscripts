import pandas as pd

# Load the two Excel files
file1_path = input('Enter file1.xlsx -> ')
file2_path = input('Enter file2.xlsx -> ')

sheet1 = input('Enter Sheet1 Name -> ')
sheet2 = input('Enter Sheet2 Name -> ')

# Load the second column from both files
column_name = input('Enter column name ') # ie Client Name/column name
df1 = pd.read_excel(file1_path, sheet_name= f'{sheet1}', usecols=[1], names=[column_name])
df2 = pd.read_excel(file2_path, sheet_name= f'{sheet2}', usecols=[1], names=[column_name])

# Find the differences between the columns
differences = pd.concat([df1, df2]).drop_duplicates(keep=False)

# Output the differences
print("\n<==================>\n")
print("Differences in the second column:")
print("\n<==================>\n")
print(differences)
print("\n")
