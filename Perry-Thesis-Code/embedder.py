import time
import json
import requests
import pandas as pd
import os
import tiktoken

# Load environment variables
EMBEDDING_ENDPOINT = os.getenv('EMBEDDING_ENDPOINT')
EMBEDDING_KEY = os.getenv('EMBEDDING_KEY')

# Check if environment variables are loaded
if not EMBEDDING_ENDPOINT or not EMBEDDING_KEY:
    raise ValueError("EMBEDDING_ENDPOINT and EMBEDDING_KEY must be set")

# Initialize the tokenizer
tokenizer = tiktoken.get_encoding("cl100k_base")

# Function to split text into chunks by tokens
def chunk_text_by_tokens(text, tokenizer, max_tokens_per_chunk=7000):
    token_ids = tokenizer.encode(text)
    chunks = [tokenizer.decode(token_ids[i:i + max_tokens_per_chunk]) for i in range(0, len(token_ids), max_tokens_per_chunk)]
    return chunks

def embed_pdf_contents(df, EMBEDDING_ENDPOINT, EMBEDDING_KEY):
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

    # Replace PDF content with embeddings
    for index, row in df.iterrows():
        if pd.notnull(row['PDF Content']):
            try:
                chunks = chunk_text_by_tokens(row['PDF Content'], tokenizer)
                embeddings = [get_embedding(chunk) for chunk in chunks]
                df.at[index, 'Embedded Papers'] = embeddings
                print(f"Processed row {index + 1}/{len(df)}")
            except requests.exceptions.HTTPError as e:
                print(f"Error processing row {index + 1}: {e}")
            time.sleep(10)  # Adjust the sleep time based on your rate limits

    # Save the updated DataFrame to a new CSV
    output_csv_path = '/Users/ian/updated_articles_with_embeddings.csv'
    df.to_csv(output_csv_path, index=False)
    print(f"Updated DataFrame saved to {output_csv_path}")

# Load the CSV file into a DataFrame
csv_file_path = '/Users/ian/updated_articles_with_normalized_content.csv'
print(f"Loading CSV file from {csv_file_path}...")
df = pd.read_csv(csv_file_path)
print("CSV file loaded successfully.")

# Call the function to embed PDF contents
print("Starting to embed PDF contents...")
embed_pdf_contents(df, EMBEDDING_ENDPOINT, EMBEDDING_KEY)
print("Embedding process completed.")