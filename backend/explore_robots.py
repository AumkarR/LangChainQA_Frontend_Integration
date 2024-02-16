import requests, zipfile
from urllib.robotparser import RobotFileParser
import gzip
import shutil
from io import BytesIO
import os
import xml.etree.ElementTree as ET
import re
import json

robots_url = "https://www.producthunt.com/robots.txt"

# store robots.txt as a string 
robots_txt_content = requests.get(robots_url).text

# make array of all urls in robots.txt  
urls_array = [line.replace("Sitemap: ", "") for line in robots_txt_content.split('\n') if line.startswith('Sitemap')]


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
    
    # Iterate over all elements in the XML
    for elem in root.iter():
        # If the element's text contains a URL, add it to the array
        if elem.text:
            found_urls = url_pattern.findall(elem.text)
            urls_array.extend(found_urls)
    
    # with open('./urls.txt', 'a') as f:
    #     f.write('\n'.join(urls))
    # print(urls)
    # return urls

    



if __name__ == "__main__":
    for url in urls_array:
        xml_file = download_and_unzip(url)
        print(f"Unzipped: {xml_file}")

        # urls array that contains all urls
        urls_array = []
        with open(xml_file, 'r') as f:
            extract_urls_from_xml(xml_file, urls_array)
        

        with open('./urls_updated.txt', 'a') as f:
            f.write('\n'.join(urls_array))