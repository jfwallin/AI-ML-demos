import pandas as pd

# Load the CSV file
df = pd.read_csv('/Users/ian/articles.csv')

# Replace 'abs' with 'pdf' in the 'PDF Link' column
df['PDF Link'] = df['PDF Link'].str.replace('abs', 'pdf')

# Save the updated DataFrame to a new CSV file
df.to_csv('/Users/ian/updated_articles.csv', index=False)

print("PDF links updated and saved to updated_articles.csv")