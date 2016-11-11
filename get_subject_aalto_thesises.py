# python3
# -*- coding: utf-8 -*-

"""
Gets all thesises listed by subjects on aaltodoc.aalto.fi website
"""

import bs4, requests

# Set the bs parser and the thesis subjects url
parser = "html.parser"
subjects_url = "https://aaltodoc.aalto.fi/doc_public/subjects/"

# Get the subjects
subjects_res = requests.get(subjects_url)
# Check that the request was successful
subjects_res.raise_for_status()

# Initialize empty list for holding the subjects and all of the thesises
subjects_list = []
all_thesises = []

# Append the subjects to the list
subjects_soup = bs4.BeautifulSoup(subjects_res.text, parser)
for tr in subjects_soup.find_all('tr', attrs={'class':'gradeC'}):
    subjects_list.append(str(tr.td.string))

for i in range(len(subjects_list)):
    # Get the url from the subject
    thesis_subject = subjects_list[i]
    thesis_url = "https://aaltodoc.aalto.fi/browse?rpp=10000&offset=0&etal=-1&sort_by=-1&type=subject&value="
    thesis_url += thesis_subject 
    thesis_url += "&order=ASC"
    
    # Get the thesises
    thesis_res = requests.get(thesis_url)
    # Check that the request was successful
    thesis_res.raise_for_status()
    
    # 
    soup = bs4.BeautifulSoup(thesis_res.text, parser)
    
    # Initialize lists for checking non-thesis words
    no_thesis_words = []
    thesises = []
    
    # Load the non-thesis words
    with open("no_thesis_words.txt", "r") as f:
        for line in f:
            no_thesis_words.append(str(line.strip('\n')))
        no_thesis_words = set(no_thesis_words)
        
    # Append the thesises to the list
    for a in soup.find_all("a", href=True):
        if a.string == None or len(a.string) < 2:
            pass
        elif a.string not in no_thesis_words:
            thesises.append(a.string)
            all_thesises.append(a.string)
    
    # Save the thesises to hard drive
    with open(thesis_subject + " thesises.txt", "w", encoding='utf-8') as save_file:
        save_file.write("Total of " + str(len(thesises)) + " thesises\n")
        for line in thesises:
            save_file.write(line+ "\n")

    
# Save all thesises to one file
with open("all_thesises.txt", "w", encoding='utf-8') as save_file:
        save_file.write("Total of " + str(len(all_thesises)) + " thesises\n")
        for line in all_thesises:
            save_file.write(line+ "\n")