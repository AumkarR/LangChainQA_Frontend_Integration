import os
import requests
from urllib.parse import urlparse #Importing urlparse to help parse url to retrieve their HTML files

subfolder = 'product_information' #Defining the subfolder that should contain the scraped HTML files
if not os.path.exists(subfolder): # Make the subfolder if it doesn't exist
    os.mkdir(subfolder)

with open('urls.txt', 'r') as url_list: # Open the urls.txt file and loop through each URL
    for url in url_list: 
        url = url.strip() # Remove any whitespace characters from the URL
        parsed_url = urlparse(url) # Parsing the URL to get the path and filename
        url_path = parsed_url.path.split('/')
        filename = url_path[-1] #Setting the filename to be the last entry of the url
        if not filename.endswith('.html'): #Ensuring that the file ends with .html to avoid errors of storing .unk files into the Chroma vectorstore
            filename += '.html'

        response = requests.get(url) #Executing a GET HTML request to retrieve a response

        # Save the HTML content to a file in the subfolder
        with open(os.path.join(subfolder, filename), 'wb') as resulting_file: #Joining the subfolder name and the pathname and opening the resulting file(resulting_file) in binary write mode
            resulting_file.write(response.content) #Writing the opened file with the content of the response from the GET request

        print(f"Downloaded {filename} to {subfolder}") #Using the 'f' keyword before the string to insert the relevant filename and subfolder in the output statement

#For time and resource saving purposes, only a few entries were parsed through the scraper as scraping over 25,000 URLs from the JCrew website would require significant processing power