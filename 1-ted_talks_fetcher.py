# Importing necessary libraries
import requests
import csv

# Define a function to fetch data from all pages of a given URL
def fetch_all_pages(url, start_page=0):
    # Initialize a list to store all video data
    all_videos_data = []
    # Set the initial page number
    page = start_page

    # Start an infinite loop to fetch data from each page
    while True:
        # Define the payload for the POST request
        payload = [
            {
                "indexName": "newest",
                "params": {
                    "attributeForDistinct": "objectID",
                    "distinct": 1,
                    "facets": [
                        "subtitle_languages",
                        "tags"
                    ],
                    "highlightPostTag": "__/ais-highlight__",
                    "highlightPreTag": "__ais-highlight__",
                    "hitsPerPage": 24,
                    "maxValuesPerFacet": 500,
                    "page": page,
                    "query": "",
                    "tagFilters": ""
                }
            }
        ]
        # Send a POST request to the URL with the payload
        response = requests.post(url, json=payload)
        # Check if the response status is not 200 (OK) and break the loop if it's not
        if response.status_code != 200:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")
            break

        # Parse the JSON response
        data = response.json()
        # Extract the 'hits' section from the response
        hits = data['results'][0]['hits']
        # Break the loop if there are no hits (data)
        if not hits:
            break

        # Iterate through each hit and extract relevant video information
        for hit in hits:
            # Construct the video URL
            video_url = f"https://www.ted.com/talks/{hit.get('slug')}" 
            # Create a dictionary of video information
            video_info = {
                "duration": hit.get("duration"),
                "title": hit.get("title"),
                "speakers": hit.get("speakers"),
                "objectID": hit.get("objectID"),
                "url": video_url
            }
            # Append the video information to the all_videos_data list
            all_videos_data.append(video_info)

        # Print the status of data fetching
        print(f"Page {page + 1} fetched. Total videos fetched: {len(all_videos_data)}")  
        # Increment the page number
        page += 1

    # Return the list of all video data
    return all_videos_data

# URL for the TED Talks data API
url = "https://zenith-prod-alt.ted.com/api/search"
# Call the function to fetch all video data
all_videos = fetch_all_pages(url)

# Define the CSV file name
csv_file = "1-all_urls.csv"
# Open the CSV file in write mode
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    # Define the field names for the CSV
    fieldnames = ['duration', 'title', 'speakers', 'objectID', 'url']
    # Create a CSV DictWriter object
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write the header to the CSV file
    writer.writeheader()
    # Write each video's data as a row in the CSV file
    for video in all_videos:
        writer.writerow(video)

# Print a confirmation message after saving the data
print(f"Data has been saved to {csv_file}")
