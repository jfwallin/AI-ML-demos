import pandas as pd
import numpy as np
import ast

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def create_similarity_matrix(df):
    num_papers = len(df)
    similarity_matrix = np.zeros((num_papers, num_papers))

    for i in range(num_papers):
        for j in range(num_papers):
            if pd.notnull(df.at[i, 'Embedded Abstract']) and pd.notnull(df.at[j, 'Embedded GPT Summary']):
                abstract_embedding = np.array(ast.literal_eval(df.at[i, 'Embedded Abstract']))
                summary_embedding = np.array(ast.literal_eval(df.at[j, 'Embedded GPT Summary']))
                similarity = cosine_similarity(abstract_embedding, summary_embedding)
                similarity_matrix[i, j] = similarity
        print(f"Completed similarity calculations for row {i + 1}/{num_papers}")

    similarity_df = pd.DataFrame(similarity_matrix, index=df.index, columns=df.index)
    return similarity_df

# Load the CSV file into a DataFrame
csv_file_path = '/Users/ian/updated_articles_with_embedded_abstracts_summaries.csv'
print(f"Loading CSV file from {csv_file_path}...")
df = pd.read_csv(csv_file_path)
print("CSV file loaded successfully.")

# Create the similarity matrix
print("Starting to create similarity matrix...")
similarity_df = create_similarity_matrix(df)
print("Similarity matrix creation completed.")

# Save the similarity matrix to a new CSV
output_csv_path = '/Users/ian/cosine_similarity_matrix.csv'
similarity_df.to_csv(output_csv_path, index=True)
print(f"Similarity matrix saved to {output_csv_path}")