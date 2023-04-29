import requests
from bs4 import BeautifulSoup #Importing BeatifulSoup library to help with scraping the URLs from the JCrew sitemap

sitemap_url = "https://www.jcrew.com/sitemap-wex/sitemap-index.xml" #The URL of the sitemap of JCrew. For added versaility, this can be replaced with the URL for any website. The robots.txt file can be used to grab the sitemap url for any website. 
response = requests.get(sitemap_url) #Executing a HTML GET request and storing the response

soup = BeautifulSoup(response.content, 'xml') #Using BeautifulSoup to store the content of the responses in the XML format
sitemap_urls = [node.text for node in soup.find_all('loc')] #Finding all sitemaps contained within the sitemap file and storing their URLs

html_urls = []
for sitemap_url in sitemap_urls: #Looping through each sitemap URL to extract the HTML URLs
    response = requests.get(sitemap_url) #Repeating the same logic for all existing sitemaps until all of the HTML files are parsed
    soup = BeautifulSoup(response.content, 'xml')
    urls = [node.text for node in soup.find_all('loc')]
    html_urls += [url for url in urls]

with open('urls.txt', 'w') as output_file: #Writing the URLs into the urls.txt file
    for url in html_urls:
        output_file.write(url + '\n')
