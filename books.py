import requests
from bs4 import BeautifulSoup
import json

# Base URL of the site, modifying this to format with different page numbers
base_url = 'https://books.toscrape.com/catalogue/page-{}.html'

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

# Loop through all 50 pages of the website
for page_num in range(1, 6):
    # Format the URL with the current page number
    url = base_url.format(page_num)

    # Send a GET request to the URL
    res = requests.get(url)
    res.encoding = 'utf-8'

    # Check if the page was fetched successfully
    if res.status_code != 200:
        print(f"Failed to retrieve data from: {url}")
        continue

    # Create a BeautifulSoup object to parse HTML
    soup = BeautifulSoup(res.text, 'html.parser')

    # Select each book entry and extract relevant information
    list_items = soup.select('ol.row li')
    for item in list_items:
        name = item.select('h3 a')[0]['title']
        price = item.select('.price_color')[0].text.strip()
        rate_class = item.select_one('.star-rating')['class'][1]  # Extract the second class attribute for the rating

        books.append({
            'name': name,
            'price': price,
            'rate': book_rate.get(rate_class, 0)  # Use get to avoid KeyError if the rating is not found
        })

# Print the number of books and some examples to verify
print(f"Total books scraped: {len(books)}")
print(books[:5])  # Show the first 5 books as a sample

# Save the extracted data to a JSON file
with open('books_data.json', 'w', encoding='utf-8') as file:
    json.dump(books, file, ensure_ascii=False, indent=4)
