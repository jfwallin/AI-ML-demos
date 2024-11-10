import time
import json
import requests
import pandas as pd
import os

# Load environment variables
EMBEDDING_ENDPOINT = os.getenv('EMBEDDING_ENDPOINT')
EMBEDDING_KEY = os.getenv('EMBEDDING_KEY')

# Check if environment variables are loaded
if not EMBEDDING_ENDPOINT or not EMBEDDING_KEY:
    raise ValueError("EMBEDDING_ENDPOINT and EMBEDDING_KEY must be set")

def embed_summaries(df, EMBEDDING_ENDPOINT, EMBEDDING_KEY):
    def get_embedding(text):
        headers = {
            "Content-Type": "application/json",
            "api-key": EMBEDDING_KEY,
        }
        data = json.dumps({
            "input": text
        })
        response = requests.post(EMBEDDING_ENDPOINT, headers=headers, data=data)
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]  # Adjust based on actual response structure

    # Create the 'Embedded GPT Summary' column
    df['Embedded GPT Summary'] = None

    # Embed summaries and create a new column
    for index, row in df.iterrows():
        if pd.notnull(row['GPT Summary']):
            try:
                embedding = get_embedding(row['GPT Summary'])
                df.at[index, 'Embedded GPT Summary'] = embedding
                print(f"Processed row {index + 1}/{len(df)}")
            except requests.exceptions.HTTPError as e:
                print(f"Error processing row {index + 1}: {e}")
            time.sleep(10)  # Adjust the sleep time based on your rate limits

    # Save the updated DataFrame to a new CSV
    output_csv_path = '/Users/ian/updated_articles_with_embedded_summaries.csv'
    df.to_csv(output_csv_path, index=False)
    print(f"Updated DataFrame saved to {output_csv_path}")

# Load the CSV file into a DataFrame
csv_file_path = '/Users/ian/updated_articles_with_summaries.csv'
print(f"Loading CSV file from {csv_file_path}...")
df = pd.read_csv(csv_file_path)
print("CSV file loaded successfully.")

# Call the function to embed summaries
print("Starting to embed summaries...")
embed_summaries(df, EMBEDDING_ENDPOINT, EMBEDDING_KEY)
print("Embedding process completed.")