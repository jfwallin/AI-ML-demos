import pandas as pd
import re

# Load the CSV file into a DataFrame
df = pd.read_csv('/Users/ian/updated_articles_with_summaries.csv')

# Function to normalize text
def normalize_text(s, sep_token=" \n "):
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r"\.\s*,", "", s)  # Fix typo here
    s = s.replace("..", ".")
    s = s.replace(". .", ".")
    s = s.replace("\n", "")
    s = s.strip()
    return s

# Normalize the text and replace it in the same column
df['GPT Summary'] = df['GPT Summary'].apply(lambda x: normalize_text(x) if pd.notnull(x) else x)

# Save the DataFrame back to CSV
df.to_csv('/Users/ian/updated_articles_with_normalized_summary.csv', index=False)
