# Script downloads anime Episode from ERAI RAWS
# Based off keywords specified in the array
# 
# Usage: Filters Magnet links based off keywords and 1080 to get 1080p
#        Begins download only if file with that keyword doesnt exist in directory specified
#        Fetches titles only if file with that keyword doesnt exist in directory specified

import re, requests, os, os.path, fnmatch
from bs4 import BeautifulSoup

#subs_please = 'https://subsplease.org/'
#nyaa_link   = 'https://nyaa.si/'
erai_raws   = 'https://www.erai-raws.info/posts/'

file_path = "F:\Downloadz"

#KEYWORDS TO SEARCH FOR WHEN SEARCHING FOR TITLE/MAGNETS
anime_titles = ["Nanatsu", "Academia", "Nomad"]

request = requests.get(erai_raws, headers={'User-Agent': 'Mozilla/5.0'})
source = request.content
soup = BeautifulSoup(source, 'lxml')

#FUNCTION TO CHECK IF EPISODE ALREADY EXISTS IN DIRECTORY
def if_episode_exists(Name, GetName):
    for file in os.listdir(file_path):
        if Name in file:
            if GetName is False:
                return True
            else:
                return file #return filename

#FETCHING TITLE NAMES
section = soup.findAll("font", {"class" : "aa_ss_blue"})
titles = []

#DATE
#date_aired = soup.findAll("font", {"class" : "clock_time_white"})

for row in section:
    desired_title = row.find('a')['data-title']
    for name in anime_titles:
        if name in desired_title:
            if if_episode_exists(name, False) is not True:
                titles.append(desired_title)            

#GET ALL MAGNETS AND FILTER OUT KEYWORDS/1080P
magnets = []
for link in soup.findAll('a', attrs={'href': re.compile("^magnet")}):
    for name in anime_titles: 
        if name in link.get('href') and "1080" in link.get('href'):
            if if_episode_exists(name, False) is not True: #if it doesnt exist in directory
                magnets.append(link.get('href'))
            else:
                print("Episode Exists:", if_episode_exists(name, True))

#START THE MAGNET DOWNLOADS
for link in magnets:
    os.startfile(link)
    print("Downloading:")
    print(titles)