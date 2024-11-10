import os
import time
import requests
import pandas as pd
import tiktoken

# Load environment variables
GPT35_KEY = os.getenv('GPT35_KEY')
GPT35_ENDPOINT = "https://wallin-openai.openai.azure.com/openai/deployments/gpt35turbowallin/chat/completions?api-version=2024-08-01-preview"

tokenizer = tiktoken.get_encoding("cl100k_base")

# Load the CSV file into a DataFrame
csv_file_path = '/Users/ian/updated_articles_with_content_embeddings.csv'
print(f"Loading CSV file from {csv_file_path}...")
df = pd.read_csv(csv_file_path)
print("CSV file loaded successfully.")

# Add a new column for GPT summaries
df['GPT Summary'] = None

# Function to chunk text
def chunk_text(text, max_tokens):
    tokens = tokenizer.encode(text)
    chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [tokenizer.decode(chunk) for chunk in chunks]

# Function to generate summary for a chunk of text
def generate_summary_for_chunk(chunk):
    headers = {
        "Content-Type": "application/json",
        "api-key": GPT35_KEY,
    }
    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following article:\n\n{chunk}"}
        ],
        "max_tokens": 150,  # Fixed output token length for summaries
        "temperature": 0.7,
    }
    response = requests.post(GPT35_ENDPOINT, headers=headers, json=data)
    response.raise_for_status()
    summary = response.json()["choices"][0]["message"]["content"]
    return summary

# Generate summaries for each row in the DataFrame
for index, row in df.iterrows():
    if pd.notnull(row['PDF Content']):
        chunks = chunk_text(row['PDF Content'], 3900)  # Adjust max_tokens as needed
        total_chunks = len(chunks)
        summaries = []
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i + 1} of {total_chunks} for row {index}...")
            summary = generate_summary_for_chunk(chunk)
            summaries.append(summary)
            time.sleep(1)  # Add a delay to avoid hitting rate limits
        df.at[index, 'GPT Summary'] = ' '.join(summaries)
        print(f"Row {index} summarized.")

# Save the updated DataFrame to a new CSV
output_csv_path = '/Users/ian/updated_articles_with_summaries.csv'
df.to_csv(output_csv_path, index=False)
print(f"Updated DataFrame with summaries saved to {output_csv_path}")