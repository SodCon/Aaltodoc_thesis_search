# python3
# -*- coding: utf-8 -*-

"""
Gets all master thesises headings listed on aaltodoc.aalto.fi website
"""

import bs4, requests

# Set the bs parser and the thesis subjects url
parser = "html.parser"
base_url = "https://aaltodoc.aalto.fi"
start_url = "https://aaltodoc.aalto.fi/handle/123456789/3/recent-submissions?offset=0"
next_url = ""
all_thesises = []

# Initialize lists for checking non-thesis words
no_thesis_words = []
# Load the non-thesis words
with open("no_thesis_words.txt", "r") as f:
    for line in f:
        no_thesis_words.append(str(line.strip('\n')))
    no_thesis_words = set(no_thesis_words)

# Get the first page
thesis_res = requests.get(start_url)
thesis_res.raise_for_status()

soup = bs4.BeautifulSoup(thesis_res.text, parser)

next_page = True
while next_page:
    next_page = False
    # Append the thesises to the list
    for a in soup.find_all("a", href=True):
        if a.string == "Next Page":
            next_url = a["href"]
            next_page = True
        if a.string == None or len(a.string) < 2:
            pass
        elif a.string not in no_thesis_words:
            all_thesises.append(a.string.strip("\n"))
    #pprint.pprint(all_thesises, width = 300)

    # Get the next page
    thesis_res = requests.get(base_url + next_url)
    thesis_res.raise_for_status()
    soup = bs4.BeautifulSoup(thesis_res.text, parser)
    
# Save all thesises to one file
with open("all_thesises.txt", "w", encoding='utf-8') as save_file:
        save_file.write("Total of " + str(len(all_thesises)) + " thesises\n")
        for line in all_thesises:
            save_file.write(line+ "\n")