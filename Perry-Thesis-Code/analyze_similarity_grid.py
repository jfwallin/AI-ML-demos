import pandas as pd

n = 40

# Load the similarity matrix CSV file into a DataFrame
similarity_csv_path = '/Users/ian/cosine_similarity_matrix.csv'
print(f"Loading similarity matrix from {similarity_csv_path}...")
similarity_df = pd.read_csv(similarity_csv_path, index_col=0)
print("Similarity matrix loaded successfully.")

# Load the articles CSV file into a DataFrame
articles_csv_path = '/Users/ian/articles.csv'
print(f"Loading articles data from {articles_csv_path}...")
articles_df = pd.read_csv(articles_csv_path)
print("Articles data loaded successfully.")

# Debug print to check columns of articles_df
print("Columns in articles_df:", articles_df.columns)

# Function to get top N highest similarity scores
def get_top_n_similarities(similarity_df, articles_df, n):
    # Melt the DataFrame to long format
    melted_df = similarity_df.reset_index().melt(id_vars='index')
    melted_df.columns = ['article1', 'article2', 'similarity']
    
    # Convert article1 and article2 to integers
    melted_df['article1'] = melted_df['article1'].astype(int)
    melted_df['article2'] = melted_df['article2'].astype(int)
    
    # Remove self-similarities and duplicate pairs
    #melted_df = melted_df[melted_df['article1'] != melted_df['article2']]
    #melted_df = melted_df[melted_df['article1'] < melted_df['article2']]
    
    # Sort by similarity score in descending order
    top_similarities = melted_df.sort_values(by='similarity', ascending=False).head(n)
    
    # Debug print to check the top similarities before merging
    print("Top similarities before merging:")
    print(top_similarities)
    
    # Merge with articles_df to get titles, bibcodes, and PDF links
    top_similarities = top_similarities.merge(articles_df, left_on='article1', right_on='Index')
    top_similarities = top_similarities.merge(articles_df, left_on='article2', right_on='Index', suffixes=('_1', '_2'))
    
    # Select relevant columns
    top_similarities = top_similarities[['article1', 'article2', 'similarity', 'Title_1', 'Bibcode_1', 'PDF Link_1', 'Title_2', 'Bibcode_2', 'PDF Link_2']]
    
    return top_similarities

# Get the top N highest similarity scores
top_similarities = get_top_n_similarities(similarity_df, articles_df, n)

# Print the top similarities
print(f"Top {n} highest similarity scores:")
print(top_similarities)

# Save the top similarities to a new CSV file
output_csv_path = f'/Users/ian/top_{n}_similarities.csv'
top_similarities.to_csv(output_csv_path, index=False)
print(f"Top similarities saved to {output_csv_path}")