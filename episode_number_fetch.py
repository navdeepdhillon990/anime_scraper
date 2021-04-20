import re, requests, os, os.path, fnmatch
from bs4 import BeautifulSoup

def get_numbers_from_filename(filename):
    number = re.search(" - (\d+)", filename).group(0)
    return re.search(r'\d+', number).group(0)

file_path = "F:\Downloadz"
anime_titles = ["Nanatsu", 
                "Academia",    
                "Nomad",
                "Shadows"]

numbers = []

for anime in anime_titles:
    for file in os.listdir(file_path):
        if anime in file:
            numbers.append(get_numbers_from_filename(file))
            doesexist = True
        else:
            doesexist = False

print(numbers)
print(doesexist)