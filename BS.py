from urllib.request import urlopen as uReq
import urllib
from bs4 import BeautifulSoup as soup
import os
import time
from tqdm import tqdm
import requests

target_url = 'http://www.duncantrussell.com/episodes/'
base_url = 'http://www.duncantrussell.com'
###########################################################################################
# This function downloads one episode with metadata
# TODO: download image, episode information
###########################################################################################
def download(url):
    print(url)
    with uReq(url) as tar_connection:
        tar_html = tar_connection.read()
    tar_soup=soup(tar_html,"html.parser")

    title= tar_soup.find("meta",{"property":"og:title"})
    print("Downloading \"" + title["content"]+"\"")
    epName="DTFH/"+title["content"]+".mp3"

    mp3_path = tar_soup.find("div", {"class": "sqs-audio-embed"})
    mp3=mp3_path["data-url"]
    response = requests.get(mp3, stream=True)

    with open(epName, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)

    print(epName + " successfully downloaded!")
###########################################################################################
# generating README
###########################################################################################
with open("README.txt", "w+") as f:
    f.write("This is a programming project by David Fentz. \n")
    f.write("The purpose is to automatically download all episodes of the DTFH podcast.\n")
    f.write("The program will create THIS README file along with a folder for all of the episodes"
        "in the directory from which it is run.\n")
    f.write("\n \n Follow the project at https://github.com/bomjumaku/DTFH_WebCrawler")

###########################################################################################
# Creating folder for files
###########################################################################################
if os.path.exists("DTFH"):
    print("The DTFH Folder already exists.")
else:
    os.makedirs("DTFH")
###########################################################################################
# Initializing variables
###########################################################################################
episode_list=[]
next_page=target_url
count =1
###########################################################################################
# Loading links for all episodes
# TODO: Make sure that each episode is unique before downloading it!
###########################################################################################
while next_page is not None:
    try:
        with uReq(next_page) as connection:
            page_html = connection.read()
        page_soup=soup(page_html,"html.parser")

        episode_list = episode_list + page_soup.findAll("p", {"class": "listen-link"})
        print("After "+ str(count) + " page(s), " + str(len(episode_list)) + " episodes were found.")
        next_link = page_soup.find("a", {"rel": "next"}) # need an if-not-null block here
        if next_link is not None:
            next_page = base_url + next_link.get('href')
        else:
            next_page=None

        count = count + 1
        time.sleep(10)

    # Handling scenario where server complains about request rate.
    except urllib.error.HTTPError as err:
        if err.code==429:
            print("Pausing for server")
            time.sleep(20)
        else:
            raise

print("We found ",str(len(episode_list))," episode links after ", count, " iterations!")
########################################################################################

url_list=[]
for each in episode_list: # Is this causing issues?
    url_list.append( base_url + each.a["href"])
for each in url_list:
    download(each)
#########################################################################################

#########################################################################################




