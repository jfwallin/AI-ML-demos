import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

def calculate_euclidean_distances(embeddings_df):
    num_points = embeddings_df.shape[0]
    distances = np.zeros((num_points, num_points))
    for i, j in combinations(range(num_points), 2):
        distance = np.linalg.norm(embeddings_df.iloc[i] - embeddings_df.iloc[j])
        distances[i, j] = distance
        distances[j, i] = distance
    return pd.DataFrame(distances)

def get_top_n_closest_pairs(distances_df, articles_df, n):
    # Get the upper triangle indices without the diagonal
    upper_triangle_indices = np.triu_indices_from(distances_df, k=1)
    
    # Extract the distances and corresponding indices
    distances = distances_df.values[upper_triangle_indices]
    indices = list(zip(upper_triangle_indices[0], upper_triangle_indices[1]))
    
    # Sort by distance
    sorted_indices = np.argsort(distances)
    
    # Select the top n closest pairs
    top_n_indices = sorted_indices[:n]
    top_n_pairs = [(indices[i][0], indices[i][1], distances[i]) for i in top_n_indices]
    
    # Create a DataFrame for the top n pairs
    top_n_df = pd.DataFrame(top_n_pairs, columns=['article1', 'article2', 'distance'])
    
    # Merge with articles_df to get titles, bibcodes, and PDF links
    top_n_df = top_n_df.merge(articles_df, left_on='article1', right_on='Index')
    top_n_df = top_n_df.merge(articles_df, left_on='article2', right_on='Index', suffixes=('_1', '_2'))
    
    # Select relevant columns
    top_n_df = top_n_df[['article1', 'article2', 'distance', 'Title_1', 'Bibcode_1', 'PDF Link_1', 'Title_2', 'Bibcode_2', 'PDF Link_2']]
    
    return top_n_df

def plot_euclidean_distances(embeddings_df, top_closest_pairs):
    plt.figure(figsize=(10, 7))
    plt.scatter(embeddings_df.iloc[:, 0], embeddings_df.iloc[:, 1], c='blue', label='Articles')
    
    for _, row in top_closest_pairs.iterrows():
        article1 = row['article1']
        article2 = row['article2']
        plt.plot([embeddings_df.iloc[article1, 0], embeddings_df.iloc[article2, 0]],
                 [embeddings_df.iloc[article1, 1], embeddings_df.iloc[article2, 1]], 'r-')
    
    plt.title('Euclidean Distance Plot')
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.legend()
    plt.show()

# Load data
embeddings_df = pd.read_csv('/Users/ian/cosine_similarity_matrix.csv', index_col=0)
articles_df = pd.read_csv('/Users/ian/articles.csv')

# Calculate Euclidean distances
distances_df = calculate_euclidean_distances(embeddings_df)

# Get the top n closest pairs
top_closest_pairs = get_top_n_closest_pairs(distances_df, articles_df, n=20)

# Plot the Euclidean distances
plot_euclidean_distances(embeddings_df, top_closest_pairs)