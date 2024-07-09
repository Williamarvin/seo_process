import requests
from bs4 import BeautifulSoup
import hashlib
import re
import json
import csv

# Specify the file path and the column name
file_path = 'output.csv'
column_name = 'link'

# Initialize an empty list to store the column data
column_data = []

# Open the CSV file and read its contents
with open(file_path, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        column_data.append(row[column_name])

# Print the list
print(len(column_data))

permalinks = column_data

# Fetch the content of the URL
with open('articles_meta.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['permalink', 'content', 'id', 'title']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    for link in permalinks:
        response = requests.get(link)
        html_content = response.content

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Get content
        content = soup.find("article")
        content = content.get_text(strip=True) if content else 'N/A'

        # Get title
        title = soup.find('title').text if soup.find('title') else 'N/A'

        # Get id
        script_tag = soup.find('script', text=re.compile(r'window.WPCOM_sharing_counts'))

        if script_tag:
            # Extract the content of the script tag
            script_content = script_tag.string

            # Use regex to find the JSON-like string within the script content
            json_data = re.search(r'window\.WPCOM_sharing_counts\s*=\s*({.*?});', script_content)
            if json_data:
                data_dict = json.loads(json_data.group(1))

                # Extract the desired value
                id = data_dict.get(link, 'N/A')
            else:
                id = 'N/A'
        else:
            id = 'N/A'

        # Write the data to the CSV file
        writer.writerow({'permalink': link, 'content': content[:1000] if len(content) > 1000 else content, 'id': id, 'title': title})
