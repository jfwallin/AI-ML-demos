import pandas as pd

# Load the CSV files into DataFrames
embeddings_csv_path = '/Users/ian/updated_articles_with_embeddings.csv'
normalized_csv_path = '/Users/ian/updated_articles_with_normalized_content.csv'

print(f"Loading CSV file from {embeddings_csv_path}...")
df_embeddings = pd.read_csv(embeddings_csv_path)
print("Embeddings CSV file loaded successfully.")

print(f"Loading CSV file from {normalized_csv_path}...")
df_normalized = pd.read_csv(normalized_csv_path)
print("Normalized CSV file loaded successfully.")

# Move the current PDF Content to a new column called Embedded Papers
df_embeddings['Embedded Papers'] = df_embeddings['PDF Content']

# Replace the PDF Content with the normalized content from the normalized DataFrame
df_embeddings['PDF Content'] = df_normalized['PDF Content']

# Save the updated DataFrame to a new CSV
output_csv_path = '/Users/ian/updated_articles_with_content_embeddings.csv'
df_embeddings.to_csv(output_csv_path, index=False)
print(f"Updated DataFrame saved to {output_csv_path}")