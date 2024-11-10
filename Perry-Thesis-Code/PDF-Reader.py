import pandas as pd
import requests
from PyPDF2 import PdfReader
import io

# Load the updated CSV file
df = pd.read_csv('/Users/ian/updated_articles.csv')

# Step 1: Add a new column 'PDF Content'
df['PDF Content'] = None

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text())
    return '\n'.join(text)  # Join the text of all pages

# Step 2: Download PDFs and extract content
for index, row in df.iterrows():
    pdf_link = row['PDF Link']  # Assuming 'PDF Link' is the correct column name
    try:
        response = requests.get(pdf_link)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Read the PDF from bytes
        pdf_reader = PdfReader(io.BytesIO(response.content))
        text_content = []
        for page in pdf_reader.pages:
            text_content.append(page.extract_text())
        df.at[index, 'PDF Content'] = '\n'.join(text_content)
    
    except Exception as e:
        print(f"Error downloading or reading {pdf_link}: {e}")

# Save the DataFrame with the new column back to CSV
df.to_csv('/Users/ian/updated_articles_with_content.csv', index=False)
