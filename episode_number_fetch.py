import re, requests, os, os.path, fnmatch
from bs4 import BeautifulSoup

def get_numbers_from_filename(filename):
    number = re.search(" - (\d+)", filename).group(0)
    return re.search(r'\d+', number).group(0)

file_path = "F:\Downloadz"
keyword = "Nomad"

for file in os.listdir(file_path):
    if keyword in file:
        numbers = get_numbers_from_filename(file)

print(numbers)