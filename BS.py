from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import os
import time
from tqdm import tqdm
import requests

my_url = 'http://www.duncantrussell.com/episodes/'
base_url = 'http://www.duncantrussell.com' # this is used to generate links with concatenation later on.

# create README
###########################################################################################
with open("README.txt", "w+") as f:
    f.write("This is a programming project by David Fentz. \n")
    f.write("The purpose is to automatically download all episodes of the DTFH.\n")
    f.write("The program will create THIS README file along with a folder for all of the episodes"
        "in the directory from which it is run.\n")
###########################################################################################
# create folder for audio files
###########################################################################################
if os.path.exists("C:/Users/User/PycharmProjects/playing/DTFH"):
    print("The DTFH Folder already exists!")
else:
    os.makedirs("DTFH")
###########################################################################################
# OPEN INITIAL PAGE


# with uReq(my_url) as connection: # open connection, grabs (downloads) page
#     page_html = connection.read()  # Read from page, store info in variable
# page_soup = soup(page_html, "html.parser")
#
# # CAPTURE INITIAL EPISODE LINKS
# episode_list = page_soup.findAll("p", {"class": "listen-link"})
# print("On first page " + str(len(episode_list)) + " episodes were found.")
episode_list=[]
next_page=my_url
count =1
########### THIS CODE LOADS ALL EPISODE LINKS
# TODO: Catch the exception for Too Many Requests and handle it with a longer wait then retry
while next_page is not None:
    with uReq(next_page) as connection:
        page_html = connection.read()
    page_soup=soup(page_html,"html.parser")

    episode_list = episode_list + page_soup.findAll("p", {"class": "listen-link"})
    print("After page", count,",",str(len(episode_list)) + " episodes were found.")
    next_link = page_soup.find("a", {"rel": "next"}) # need an if-not-null block here
    if next_link is not None:
        next_page = base_url + next_link.get('href')
        print("Next page is ", next_page)
    else:
        next_page=None
    
    count = count + 1
    time.sleep(15)
###########################################
print("We found ",str(len(episode_list))," episode links after ", count, " iterations!")

############################################################# download one mp3
# episode_info = base_url + episode_list[0].a["href"]
# print("Opening " + episode_info + " to retrieve audio file")
# with uReq(episode_info) as connection:
#     episode_html = connection.read()
#
# episode_soup = soup(episode_html,"html.parser")
# mp3_chunk = episode_soup.find("div", {"class": "sqs-audio-embed"})
# mp3=mp3_chunk["data-url"]
#
#
# response = requests.get(mp3, stream=True)
#
# with open("DTFH/TEST", "wb") as handle:
#     for data in tqdm(response.iter_content()):
#         handle.write(data)
#
# print("Download Finished!")
#####################################################################
# print(episode_html)
for each in episode_list:
    print("Opening connection to:  ", base_url + each.a["href"])

# print("\n" ,len(episode_list), " episodes downloaded in total")


