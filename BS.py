from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import os
import time
from tqdm import tqdm
import requests

target_url = 'http://www.duncantrussell.com/episodes/'
base_url = 'http://www.duncantrussell.com'
###########################################################################################
# This function downloads one episode with metadata
#TODO: download image, episode information
def download(url):
    print(url)
    with uReq(url) as tar_connection:
        tar_html = tar_connection.read()
    tar_soup=soup(tar_html,"html.parser")

    title= tar_soup.find("meta",{"property":"og:title"})
    print("Downloading " + title["content"])
    epName="DTFH/"+title["content"]+".mp3"

    mp3_path = tar_soup.find("div", {"class": "sqs-audio-embed"})
    mp3=mp3_path["data-url"]
    response = requests.get(mp3, stream=True)

    with open(epName, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)

    print(epName + " successfully downloaded!")

#####################################################################
# generating README
###########################################################################################
with open("README.txt", "w+") as f:
    f.write("This is a programming project by David Fentz. \n")
    f.write("The purpose is to automatically download all episodes of the DTFH.\n")
    f.write("The program will create THIS README file along with a folder for all of the episodes"
        "in the directory from which it is run.\n")
###########################################################################################
# Creating folder for files
###########################################################################################
if os.path.exists("DTFH"):
    print("The DTFH Folder already exists.")
else:
    os.makedirs("DTFH")
###########################################################################################
# Initializing variables
episode_list=[]
next_page=target_url
count =1
# Loading links for all episodes
###########################################################################################
# TODO: Catch the exception for Too Many Requests and handle it with a longer wait then retry
# while next_page is not None:
#     with uReq(next_page) as connection:
#         page_html = connection.read()
#     page_soup=soup(page_html,"html.parser")
#
#     episode_list = episode_list + page_soup.findAll("p", {"class": "listen-link"})
#     print("After page", count,",",str(len(episode_list)) + " episodes were found.")
#     next_link = page_soup.find("a", {"rel": "next"}) # need an if-not-null block here
#     if next_link is not None:
#         next_page = base_url + next_link.get('href')
#         print("Next page is ", next_page)
#     else:
#         next_page=None
#
#     count = count + 1
#     time.sleep(15)

# print("We found ",str(len(episode_list))," episode links after ", count, " iterations!")

# for each in episode_list: # Is this causing issues?
#     each= base_url + each.a["href"]
#########################################################################################
# Test code for developing the download function
with uReq(next_page) as connection:
    page_html = connection.read()
page_soup=soup(page_html,"html.parser")

episode_list = episode_list + page_soup.findAll("p", {"class": "listen-link"})
print("After page", count,",",str(len(episode_list)) + " episodes were found.")

target_ep= base_url + episode_list[0].a["href"]

#########################################################################################
download(target_ep)
#########################################################################################




