import os
import json
import requests
import pandas as pd
import time

# Load environment variables
QUERY_ENDPOINT = os.getenv('QUERY_ENDPOINT')
QUERY_KEY = os.getenv('QUERY_KEY')

# Check if environment variables are loaded
if not QUERY_ENDPOINT or not QUERY_KEY:
    raise ValueError("QUERY_ENDPOINT and QUERY_KEY must be set")

def query_llm(content, QUERY_ENDPOINT, QUERY_KEY):
    headers = {
        "Content-Type": "application/json",
        "api-key": QUERY_KEY,
    }
    data = json.dumps({
        "prompt": f"Is this article about the Milky Way? {content}",
        "max_tokens": 100  # Adjust based on your needs
    })
    response = requests.post(QUERY_ENDPOINT, headers=headers, data=data)
    response.raise_for_status()
    return response.json()  # Adjust based on actual response structure

def find_articles_about_milky_way(df, QUERY_ENDPOINT, QUERY_KEY):
    results = []
    for index, row in df.iterrows():
        if pd.notnull(row['PDF Content']):
            try:
                response = query_llm(row['PDF Content'], QUERY_ENDPOINT, QUERY_KEY)
                answer = response['choices'][0]['text'].strip()  # Adjust based on actual response structure
                if "yes" in answer.lower():
                    results.append((index, row['Title'], answer))
                print(f"Processed row {index + 1}/{len(df)}")
            except requests.exceptions.HTTPError as e:
                print(f"Error processing row {index + 1}: {e}")
            time.sleep(1)  # Adjust the sleep time based on your rate limits
    return results

# Load the CSV file into a DataFrame
csv_file_path = '/Users/ian/updated_articles_with_normalized_content.csv'
print(f"Loading CSV file from {csv_file_path}...")
df = pd.read_csv(csv_file_path)
print("CSV file loaded successfully.")

# Call the function to find articles about the Milky Way
print("Starting to query articles about the Milky Way...")
results = find_articles_about_milky_way(df, QUERY_ENDPOINT, QUERY_KEY)
print("Query process completed.")

# Display the results
for index, title, answer in results:
    print(f"Article {index} titled '{title}' is about the Milky Way: {answer}")