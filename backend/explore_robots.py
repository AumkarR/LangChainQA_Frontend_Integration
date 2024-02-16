import requests
from urllib.robotparser import RobotFileParser
import gzip
import shutil
from io import BytesIO
import os
import xml.etree.ElementTree as ET
import re
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import concurrent.futures
from urllib.parse import urlparse #Importing urlparse to help parse url to retrieve their HTML files


robots_url = "https://www.producthunt.com/robots.txt"

# store robots.txt as a string 
robots_txt_content = requests.get(robots_url).text

# make array of all urls in robots.txt  
overall_urls = [line.replace("Sitemap: ", "") for line in robots_txt_content.split('\n') if line.startswith('Sitemap')]


def download_and_unzip(url):
    filename = url.split('/')[-1]
    path_to_gz = f"./zip_files/{filename}"
    path_to_xml = path_to_gz[:-3]  # Removing '.gz'

    # Downloading the file
    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    with open(path_to_gz, 'wb') as f:
        f.write(response.content)

    print(f"Unzipping {filename}...")
    with gzip.open(path_to_gz, 'rb') as f_in:
        with open(path_to_xml, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    os.remove(path_to_gz)

    return path_to_xml

def extract_urls_from_xml(xml_file_path, urls_array):
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    
    # Regular expression to match URLs
    url_pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
    
    # Array to store the URLs
    
    for elem in root.iter():
        # If the element's text contains a URL, add it to the array
        if elem.text:
            found_urls = url_pattern.findall(elem.text)
            urls_array.extend(found_urls)

def extract_name_and_description(urls_array):
    url_data = []

    def process_url(url):
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        title = soup.title.string
        description = soup.find('meta', attrs={'name': 'description'}).get('content')
        links = [link.get('href') for link in soup.find_all('a') if link.get('href').startswith(("http://", "https://")) and not link.get('href').endswith(("producthunt", "producthunt.com", "ProductHunt")) and not link.get('href') == "https://www.youtube.com/channel/UCOtU18DT8csQVqHPT1wtYzw" and not link.get('href') == "https://product-hunt.breezy.hr/"]
        url_data.append({
            "url": url,
            "title": title,
            "description": description,
            "links": links
        })

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(process_url, urls_array), total=len(urls_array), leave = True))  # add a progress bar in tqdm

    with open('url_data.json', 'w') as file:
        json.dump(url_data, file, indent=4)

if __name__ == "__main__":

    # EXTRACTING URLS
    return_array = []

    for url in overall_urls:
        xml_file = download_and_unzip(url)
        print(f"Unzipped: {xml_file}")

        # urls array that contains all urls
        urls_array = []
        with open(xml_file, 'r') as f:
            extract_urls_from_xml(xml_file, urls_array)
        

        urls_array = [url for url in urls_array if url.startswith("https://www.producthunt.com/products/") and not url.endswith(("/reviews", "/jobs" ,"/addons"))]

        # export_urls_as_html(urls_array)
        return_array += urls_array


    extract_name_and_description(return_array[:1024])

        # with open('./urls_updated.txt', 'a') as f:
        #     f.write('\n'.join(urls_array))


    ## PARSING URLS
    # with open('backend/urls_updated.txt', 'r') as f:
    #     urls_array = f.readlines()
    # print('\n'.join(urls_array))


        