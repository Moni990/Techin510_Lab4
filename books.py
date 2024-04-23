# This script installs necessary Python packages, parses HTML content from a URL, extracts specific data,
# and writes the output to a JSON file.

# Install necessary packages
# !pip install requests
# !pip install beautifulsoup4

import requests
from bs4 import BeautifulSoup
import json

# Define the URL from which to fetch the content
URL = 'https://books.toscrape.com/catalogue/page-1.html'

# Send a GET request to the URL
res = requests.get(URL)
res.encoding = 'utf-8'

# Create a BeautifulSoup object to parse HTML
soup = BeautifulSoup(res.text, 'html.parser') # Alternatively use 'lxml' as the parser

# Prepare to store the extracted data
books = []

# Dictionary to convert rating classes to numerical values
book_rate = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
}

# Select each book entry and extract relevant information
list_items = soup.select('ol.row li')
for item in list_items:
    name = item.select('h3 a')[0].text.strip()
    price = item.select('.price_color')[0].text.strip()
    rate = item.select('.star-rating')[0]['class'][1]  # Extract the second class attribute for the rating

    books.append({'name': name, 'price': price, 'rate': book_rate[rate]})

# Print extracted books data
print(books)

# Save the extracted data to a JSON file
with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(books, file, ensure_ascii=False, indent=4)

