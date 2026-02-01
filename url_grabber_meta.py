# Given a URL, scrape all information from the AO3 novels to write to 'notmaturecorrect.csv'.

import subprocess
import requests
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, HTTPError
from time import sleep
import csv 
import pandas as pd
from unidecode import unidecode

#
# The get_url_data function downloads the HTML at a given URL.
# Dependencies: Returns the HTML data.
# Arguments: 'url' is the given url used to grab HTML data.
#
def get_url_data(url = ""):
    try:
        request = Request(url, headers = {'User-Agent' :\
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})
        #print(request)
        response = urlopen(request)
        data = response.read().decode("utf8", errors='ignore')
        return data
    except HTTPError as e:
        #print(url)
        print(e)
        return str(e)

#
# The extract_text function grabs the body text from the scraped HTML.
# Dependencies: Takes in the novel data, returns the text extracted from the novel.
# Arguments: 'soup' is the scraped novel data.
#
def extract_text(soup): 
    try:
        # this code block is from AO3Scraper's get_fanfics.py (https://github.com/radiolarian/AO3Scraper/blob/master/ao3_get_fanfics.py): 
        body_texts = soup.find("div", id= "chapters")
        paragraph_texts = body_texts.select('p')
        text = '\n\n'.join([unidecode(p.text) for p in paragraph_texts])
        return text
    except Exception as e:
        print("Unable to extract novel text :[ ")
        #print(url)
        print(e)
        return ""

#
# The extract_author function grabs the author from the scraped HTML.
# Dependencies: Takes in the novel data, returns the author that wrote the novel.
# Arguments: 'soup' is the scraped novel data.
#
def extract_author(soup): 
    try:
        find_author = soup.find("a", rel= "author")
        author = find_author.get_text(strip=True)
        return author
    except Exception as e:
        print("Unable to extract author :[ ")
        #print(url)
        print(e)
        return ""

    #return author

#
# The extract_title function grabs the title from the scraped HTML.
# Dependencies: Takes in the novel data, returns the title of the novel.
# Arguments: 'soup' is the scraped novel data.
#
def extract_title(soup): 
    try:
        find_title = soup.find("h2", class_="title heading")
        title = find_title.get_text(strip=True)
        return title
    except Exception as e:
        print("Unable to extract novel title :[ ")
        #print(url)
        print(e)
        return ""

    #return title

#
# The extract_wordcount function grabs the number of words from the scraped HTML.
# Dependencies: Takes in the novel data, returns the number of words in the novel.
# Arguments: 'soup' is the scraped novel data.
#
def extract_wordcount(soup):
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    try: 
        find_wordcount = soup.find("dd", class_="words")
        wordcount = find_wordcount.get_text(strip = True)
        return wordcount
    except Exception as e: 
        print("Unable to extract word count")
        #print(url)
        print(e)
        return ""
    #return wordcount

#
# The extract_fandom function grabs the fandom of the scraped HTML.
# Dependencies: Takes in the novel data, returns the fandom of the novel.
# Arguments: 'soup' is the scraped novel data.
#
def extract_fandom(soup):
    try:
        find_fandom = soup.find("dd", class_= "fandom tags")
        fandom_list = find_fandom.find_all("a", class_= "tag")
        fandom = ','.join([unidecode(f.text) for f in fandom_list])
        return fandom
    except Exception as e:
        print("Unable to extract fandom")
        #print(url)
        print(e)
        return ""

#
# The extract_category function grabs the category from the scraped HTML.
# Dependencies: Takes in the novel data, returns the category of the novel.
# Arguments: 'soup' is the scraped novel data.
#
def extract_category(soup): 
    try: 
        find_category = soup.find("dd", class_="category tags")
        cat_list = find_category.find_all("a", class_= "tag")
        category = ','.join([unidecode(c.text) for c in cat_list])
        return category
    except Exception as e: 
        print("Unable to extract category")
        #print(url)
        print(e)
        return ""

#
# The extract_data function grabs the work_id, body text, author, title, word count, fandom, and category utelizing all the above functions.
# Dependencies: Takes in the novel and URL and turns it into soup, then places into a data dictionary to be returned.
# Arguments: Takes in the novel and URL.
#
def extract_data(url, novel):
    html = get_url_data(url)
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    data = {'work_id': novel, 
            'body': extract_text(soup), 
            'author': extract_author(soup), 
            'title': extract_title(soup),
            'words': extract_wordcount(soup), 
            'fandom': extract_fandom(soup), 
            'category': extract_category(soup)}
    return data

def main():
    #obtain ids
    with open('notmaturecorrect_meta.csv', 'r') as f:
        ids = [row[0] for row in csv.reader(f)]

    #write to csv
    with open('notmaturecorrect.csv', 'w', newline="") as f:
        #fieldnames = ['work_id','body']
        fieldnames = ['work_id','body', 'author', 'title', 'words', 'fandom', 'category']
        writer = csv.DictWriter(f, fieldnames = fieldnames, quoting=csv.QUOTE_NONNUMERIC) 
        writer.writeheader()
        
        count = 0 
        #scrape each fanfic 
        for novel in ids: 
            count += 1
            print('scraping ID: ', novel, " count: ", count)
            url = "https://archiveofourown.org/works/"+novel+'?view_adult=true&view_full_work=true'
            writer.writerow(extract_data(url, novel))
            print("done writing", novel)
            sleep(2)
    
main()
print("All done!")    
