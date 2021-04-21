# Script downloads anime Episode from ERAI RAWS
# Based off keywords specified in the array
# 
# Usage: Filters Magnet links based off keywords and 1080 to get 1080p
#        Simply add whatever keywords from anime title into array (and make sure that anime is supported by erai raws)
#        Begins download only if file with that keyword doesnt exist in directory specified and compared episode numbers as well

import re, requests, os, os.path, fnmatch
from bs4 import BeautifulSoup

erai_raws = 'https://www.erai-raws.info/posts/'
file_path = "F:\Downloadz"

#ANIME TITLES TO DOWNLOAD 
#NOTE: Make sure each name has a comma at the end or else the item will be ignored
anime_titles = ["Nanatsu no Taizai", 
                "Boku no Hero Academia",    
                "Megalo Box 2",
                "Bishounen"]

request = requests.get(erai_raws, headers={'User-Agent': 'Mozilla/5.0'})
source = request.content
soup = BeautifulSoup(source, 'lxml')

#---FUNCTIONS---#

#Color code text
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# checks to see if episode aired and returns true/false IF ep_num is not requested
# otherwise sends the episode number to be compared

def if_episode_aired(anime1,ep):
    for title in title_and_episode:
        if anime1 in title:
            if ep is True:
                ep_num = re.search(" - (\d+)", title).group(0)
                ep_num2 = re.search(r'\d+', ep_num).group(0)
                return ep_num2
            else:
                 return True
    return False

def get_episode_index(anime2):
    for ind, value in enumerate(title_and_episode):
        if anime2 in value:
            return ind

#-----------FETCHING ALL LATEST RELEASE INFORMATION------------#

#Fetch tags containing titles/ep number
section = soup.findAll("article", {"class" : "era_center col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12 nonmain border_radius_22"})

#Fetch "Today" Tags signifying if episode aired today
today_tags = []

for item in section:
    tags = item.findAll(attrs={"class" : "clock_time_green"})
    for x in tags:
        today_tags.append(x.text.strip())


#Grab new releases titles and episode numbers
titles = []
for row in section:
    
    #Find matching tags to get title/episode number
    new_titles = row.findAll(attrs={"class" : "aa_ss_ops"})

    #Strip the tags away to get the text and append to array
    for tag in new_titles:
        titles.append(tag.text.strip())

#Sort the array and attach anime title to episode number and store inside a new array and print
title_and_episode = []

for idx, val in enumerate(titles):
    try:
        full_title = (titles[idx] + " - " + titles[idx+1])
        title_and_episode.append(full_title)
        try:
            titles.remove(titles[idx+1])
        except:
            print("Next index is null")
    except:
        print("List End")

#Get all magnets on the episode lists
magnets = []

for link in soup.findAll('a', attrs={'href': re.compile("^magnet")}):
    if "1080" in link.get('href'):
        magnets.append(link.get('href'))

#------------ VV OUTPUT VV ----------------------#

files_were_downloaded = False

for name in anime_titles:

    #Boolean Variables 
    did_air = if_episode_aired(name,False)
    aired_num = if_episode_aired(name,True)

    for file in os.listdir(file_path):
        if name in file:
            does_exist = True
            number = re.search(" - (\d+)", file).group(0)
            file_num = re.search(r'\d+', number).group(0)
            break
        else:
            does_exist = False

    #Array index to fetch titles/magnet/air time
    ep_index = get_episode_index(name)

    #Check if index has "Today" tag, IF index exists, otherwise just store "None"
    try:
        aired_today = today_tags[ep_index]
    except:
        aired_today = "None"

    if did_air is True and "Today" in aired_today: # did a new episode air today
        if does_exist is False: #and doesnt exist in directory
            files_were_downloaded = True
            print(bcolors.OKGREEN + "Episode", aired_num, "of", name, "aired today! ┗(•̀へ •́ ╮ )" + bcolors.ENDC)
            print(bcolors.OKCYAN + "Downloading:" , name, aired_num + bcolors.ENDC)
            target_magnet = get_episode_index(name)
            os.startfile(magnets[target_magnet])
        else: #does exist in directory
            if aired_num not in file_num: #if episode number is different, start download
                print(bcolors.OKCYAN + "Downloading:" , name, aired_num, file_num + bcolors.ENDC)
                target_magnet = get_episode_index(name)
                os.startfile(magnets[target_magnet])
            else:
                print(bcolors.WARNING + name , file_num, "already exists." + bcolors.ENDC)
if files_were_downloaded is False:
    print(bcolors.WARNING + "Nothing aired today... ( ꒪Д꒪)ノ " + bcolors.ENDC)