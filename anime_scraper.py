# Anime Episode Scraper
# Richter / Deepak
# 
# Usage: Enter keywords for anime title in anime_titles array
# Can scrap Nyaa and SubsOnly based on option picked

import re, requests, os
from bs4 import BeautifulSoup

nyaa_link = 'https://nyaa.si/'
subs_only = 'https://subsplease.org/'

#KEYWORDS TO SEARCH FOR WHEN SEARCHING FOR TITLE/MAGNETS
anime_titles = ["Nanatsu", "Boku no Hero", "Nomad", "Aimer"]

request = requests.get(nyaa_link, headers={'User-Agent': 'Mozilla/5.0'})
source = request.content
soup = BeautifulSoup(source, 'lxml')

#GETTING TORRENT NAMES
title = []
rows = soup.findAll("td", colspan="2")
for row in rows:
#FIND TITLES
    desired_title = row.find('a')['title']
    for name in anime_titles:
        if name in desired_title:
            title.append(desired_title)

#GETTING MAGNET LINKS
#Searches the entire magnet link for the keywords specified earlier
magnets = []
for link in soup.findAll('a', attrs={'href': re.compile("^magnet")}):
    for name in anime_titles: 
        if name in link.get('href'):
            magnets.append(link.get('href'))

#START THE MAGNET DOWNLOADS
for link in magnets:
    os.startfile(link)
    magnets.remove(link)

print("Now downloading", title)