# Importing necessary libraries
import csv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Define a function to fetch additional data from a given URL
def fetch_additional_data(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Parse the response content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Nested function to extract text based on a specific selector
    def get_text_or_default(selector, default='', split=None, strip_chars=None):
        element = soup.find(attrs=selector)
        if element:
            text = element.text.strip()
            if strip_chars:
                text = text.strip(strip_chars)
            if split:
                text = text.split(split)[0]
            return text
        return default

    # Extract various data points from the page
    view_count = get_text_or_default({'data-testid': 'talk-view-count'}, split=' ')
    release_date = get_text_or_default({'data-testid': 'talk-release-date'}, strip_chars='•')
    context = get_text_or_default({'data-testid': 'talk-context'})
    description = get_text_or_default({'data-testid': 'talk-description-text'})

    # Extract topics/tags and format them
    topics = [a.get_text(strip=True) for a in soup.find_all('a', class_='underline')]
    tag = ', '.join(topics)

    # Return the extracted data as a dictionary
    return {
        "view": view_count,
        "date": release_date,
        "context": context,
        "description": description,
        "tag": tag,
    }

# Specify the input and output CSV filenames
input_filename = '1-all_urls.csv'
output_filename = '2-all_talks.csv'

# Open the input and output CSV files for reading and writing respectively
with open(input_filename, 'r', newline='', encoding='utf-8') as infile, \
     open(output_filename, 'w', newline='', encoding='utf-8') as outfile:

    # Create a CSV reader for the input file
    reader = csv.DictReader(infile)
    # Define the field names for the output file
    existing_fieldnames = list(reader.fieldnames) if reader.fieldnames else []
    fieldnames = existing_fieldnames + ['view', 'date', 'context', 'description', 'tag']
    # Create a CSV writer for the output file
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate over each row in the input file
    for row in tqdm(reader, desc='Processing URLs'):
        url = row['url']
        try:
            # Fetch additional data for each URL
            additional_data = fetch_additional_data(url)
            # Update the row with the additional data
            row.update(additional_data)
            # Write the updated row to the output file
            writer.writerow(row)
        except Exception as e:
            # Print any error encountered during processing
            print(f"Error processing {url}: {e}")
