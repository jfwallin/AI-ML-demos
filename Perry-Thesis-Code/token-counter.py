import pandas as pd
import tiktoken

# Load the CSV file into a DataFrame
df = pd.read_csv('/Users/ian/updated_articles_with_filled_contents.csv')

# Token counter function
def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# Specify the encoding name (e.g., "gpt2")
encoding_name = "gpt3.5"  # Change to the appropriate encoding as needed

# Count tokens for each PDF content and print index and token count
for index, row in df.iterrows():
    pdf_content = row['PDF Content']
    if pd.notnull(pdf_content):
        token_count = num_tokens_from_string(pdf_content, encoding_name)
        print(f"Index: {index} - Token Count: {token_count}")
