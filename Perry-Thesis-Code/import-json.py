import json
import pandas as pd
import ast

# Load the JSON data from the file
with open('/Users/ian/output.json', 'r') as f:
    data = json.load(f)

# Extracting relevant information
articles = data['response']['docs']
article_data = []

#print("Number of articles found:", len(articles))

for article in articles:
    title = article['title'][0] if article['title'] else 'No Title'
    abstract = article.get('abstract', 'No abstract available')
    bibcode = article.get('bibcode', 'No Bibcode available')
    
    # Extracting PDF links from links_data
    pdf_url = None
    for link in article['links_data']:
        link_dict = json.loads(link)
        #print("Link data:", link_dict)  # Check the link data
        if link_dict.get('type') in ['pdf', 'preprint']:  # Adjusted check
            pdf_url = link_dict.get('url', 'No URL available')
            break

    # Only add the article if a PDF is available
    if pdf_url:
        article_data.append({
            'Title': title,
            'Abstract': abstract,
            'Bibcode': bibcode,
            'PDF Link': pdf_url
        })

    # Stop if we have 100 articles with PDFs
    if len(article_data) >= 100:
        break

# Create DataFrame
df = pd.DataFrame(article_data)

# Add index column
df.reset_index(drop=False, inplace=True)
df.rename(columns={'index': 'Index'}, inplace=True)

# Save to a CSV file
df.to_csv('/Users/ian/articles.csv', index=False)

print("Data saved to articles.csv")
