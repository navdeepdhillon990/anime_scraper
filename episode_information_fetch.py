import re, requests, os, os.path, fnmatch
from bs4 import BeautifulSoup

erai_raws   = 'https://www.erai-raws.info/posts/'
file_path = "F:\Downloadz"

#ANIME TITLES TO DOWNLOAD
anime_titles = ["Nanatsu", 
                "Academia",    
                "Nomad",
                "Shadows"]

request = requests.get(erai_raws, headers={'User-Agent': 'Mozilla/5.0'})
source = request.content
soup = BeautifulSoup(source, 'lxml')

#---FUNCTIONS---#

# checks to see if episode aired and returns true/false IF ep_num is not requested
# otherwise sends the episode number to be compared

def if_episode_aired(anime,ep):
    for title in title_and_episode:
        if anime in title:
            if ep is True:
                ep_num = re.search(" - (\d+)", title).group(0)
                ep_num2 = re.search(r'\d+', ep_num).group(0)
                return ep_num2
            else:
                 return True
    return False

def get_episode_index(anime):
    for ind, value in enumerate(title_and_episode):
        if anime in value:
            return ind

# does the same as the top, however it searches for episode number in the anime episode 
# of the same name FOUND IN DIRECTORY specified above

def get_numbers_from_filename(filename):
    number = re.search(" - (\d+)", filename).group(0)
    return re.search(r'\d+', number).group(0)

def get_episode_exists(anime, return_ifexists):
    for file in os.listdir(file_path):
        if anime in file:
            if return_ifexists is False:
                return True
            else:
                episode = get_numbers_from_filename(file)
                return episode
        else:
            return False


#----FETCHING ALL LATEST RELEASE INFORMATION--------#

#Fetch tags containing titles/ep number
section = soup.findAll("article", {"class" : "era_center col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12 nonmain border_radius_22"})

#TAKE OUT NEW RELEASE TITLES AND EPISODE NUMBER

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

#GET ALL MAGNETS ON EPISODE LIST
magnets = []

for link in soup.findAll('a', attrs={'href': re.compile("^magnet")}):
    if "1080" in link.get('href'):
        magnets.append(link.get('href'))

#------------------------------

for name in anime_titles:
    #Boolean Variables 
    did_air = if_episode_aired(name,False)
    does_exist = get_episode_exists(name, False)

    #Episode numbers
    aired_num = if_episode_aired(name,True)
    file_num = get_episode_exists(name, True)

    #Array index to fetch titles/magnet
    ep_index = get_episode_index(name)

    #check if episode aired, and if episode exists in directory
    #if did_air is True and does_exist is False:
    #    print("Downloading:" , name, aired_num)
    #    target_magnet = get_episode_index(name)
    #    os.startfile(magnets[target_magnet])
    #elif did_air is True and does_exist is True:
    #    if aired_num not in file_num:  
    #        print("Downloadiddng:" , name, aired_num, file_num)
    #        target_magnet = get_episode_index(name)
    #        os.startfile(magnets[target_magnet])
    #    else:
    #       print(name , "already exists.")

    print("Did Air:", did_air)
    print("Does Exist:", does_exist)

    print("Aired Num:",aired_num)
    print("FileNum:",file_num)