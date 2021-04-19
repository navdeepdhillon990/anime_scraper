import re, requests, os, os.path, fnmatch
from bs4 import BeautifulSoup

#subs_please = 'https://subsplease.org/'
#nyaa_link   = 'https://nyaa.si/'
erai_raws   = 'https://www.erai-raws.info/posts/'

file_path = "F:\Downloadz"

#KEYWORDS TO SEARCH FOR WHEN SEARCHING FOR TITLE/MAGNETS
anime_titles = ["Nanatsu", "Academia", "Nomad", "Hetalia"]

request = requests.get(erai_raws, headers={'User-Agent': 'Mozilla/5.0'})
source = request.content
soup = BeautifulSoup(source, 'lxml')

#----FETCHING ALL LATEST RELEASE INFORMATION--------#

#Fetch Titles
section = soup.findAll("article", {"class" : "era_center col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12 nonmain border_radius_22"})

#TAKE OUT NEW RELEASE TITLES
titles = []
for row in section:

    #desired_episode2 = row.findAll('a', {'class' : 'tooltip2_red'})

    #desired_episode2 = row.findAll('a', {'class' : 'tooltip2_red'})
    desired_episode2 = row.findAll(attrs={"class" : "aa_ss_ops"})

    #for name in anime_titles:
    #    if name not in desired_episode2:
    #        titles.append(desired_episode2) 

    for tag in desired_episode2:
        titles.append(tag.text.strip())

for idx, val in enumerate(titles):
   print(titles[idx], " - ", titles[idx+1])

#print ([item["data-title"] for item in row.find_all() if "data-title" in item.attrs])