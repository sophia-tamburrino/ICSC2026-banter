import os
import csv
import re
from openpyxl.workbook import Workbook
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import numpy as np
import random

def get_pairs(body_path, meta_path):

    # create dialogue + meta data list
    pairs = [["Dialogue", "Response"]]
    
    # pairs_meta = [["Number", "Dialogue", "Response", "URL", "hash", "num_pairs", "work_id", "author", 
    #          "rating", "category", "fandom", "relationship", 
    #          "character", "additional tags", "language", 
    #          "published", "status", "status date",
    #          "words", "chapters", "comments", "kudos", "bookmarks",
    #          "hits", "all_kudos"]]

    #'work_id': novel, 'body': text, 'author': author, 'title': title,'words': wordcount, 'fandom': fandom, 'category': category
    pairs_meta = [["Number", "Dialogue", "Response", "URL", "hash", "num_pairs", "work_id", "title", "author", "fandom", "words","category"]]

    # save csv to a dataframe
    body_df = pd.read_csv(body_path, encoding="cp1252")
    meta_df = pd.read_csv(meta_path, header=None, names=['work_id', 'url'], encoding="cp1252")
    num = 1
    # iterate through each row (novel) in the csv
    for i, row in body_df.iterrows():

        if (row['work_id'] != 6848920) and (row['work_id'] != 35255137) and (row['work_id'] != 6953299) and (row['work_id'] != 17745707) and (row['work_id'] != 20062966):
            # get the title
            #title = row['title']
            # replace illegal characters to fix filename generation
            #title = title.replace("/", "-")
            #title = title.replace("\"", "") #DEBUG STATEMENT - Sophia
            #title = title.replace("?", "") #DEBUG STATEMENT - Sophia
            # create a text file to store the body text in

            # replace title with work id for now - Jess
            id = row['work_id']
            print(i, id) #DEBUG STATEMENT - Jess
            dir = "body-text/"
            filename = dir + str(id) + "_body.txt"
            #print(filename) DEBUG STATEMENT - Sophia
            text = row["body"]  
            #text = row["words"]

            if not os.path.exists(dir):
                os.makedirs(dir)

            # save the text to a .txt file  
            with open(filename, "w") as w:
                #print(type(text)) #DEBUG - Jess
                w.write(str(text)) ##DEBUG - had to cast text to str?? (Jess)

            # remove whitespaces to allow for easy comparison of lines
            clean_text = filename + "_clean"
            with open(filename, 'r') as r, open (clean_text, 'w') as o:
                for line in r:
                    if line.strip():
                        o.write(line)
            

            # read line by line and check for dialogue pairs
            with open(clean_text, 'r') as file:
                # save lines to a list
                lines = file.readlines()
                temp_pairs = ["temp"]
                pairs_count = -1
                for index, line in enumerate(lines):
                    # make sure lines are in bounds 
                    if index + 1 < len(lines):
                        # if the line has a quotation
                        # if pairs_count == 100:
                        #     break
                        if (lines[index].strip().count("\"") >= 2):
                            # for use of not grabbing duplicates
                            #in_list = 0
                            # try:
                            #     a = temp_pairs.index(lines[index].strip())
                            #     #print(a)
                            # except ValueError:
                            #     in_list = 0
                            
                            #if in_list == 0:
                                dialogue1 = lines[index].strip()
                                temp_pairs.append(dialogue1)
                                # find the next possible line that has dialogue
                                in_between = 0 # for use of counting the lines of writing in between dialouge
                                for i, line2 in enumerate(lines):
                                    #if (i > index) and (in_between < 5): #DEBUG - JESS
                                    if (i > index) and (in_between < 3): # HERE is where we will add our in_between variable. Ex: if (i > index) and (in_between <= 4). Will have to add another if statement if in_between breaches our limit
                                        if lines[i].strip().count("\"") >= 2:
                                            # for use of not grabbing duplicates
                                            # in_list_2 = 1
                                            # try:
                                            #     a = temp_pairs.index(lines[i].strip())
                                            #     #print(a)
                                            # except ValueError:
                                            #     in_list_2 = 0

                                            # if in_list_2 == 0:
                                                dialogue2 = lines[i].strip()
                                                temp_pairs.append(dialogue2)
                                                pairs_count += 1

                                                #if row["work_id"] == 14857223: 
                                                #    print("Dialogue 1: " + dialogue1)
                                                #    #print("In Between: " + str(in_between))
                                                #    print("Dialogue 2: " + dialogue2)

                                                pairs.append([dialogue1, dialogue2])
                                
                                                # convert author column from list representation to actual list (removes ['author_name'])
                                                # = re.sub(r"[\[\]\'\"]", "", row["author"])

                                                #add dialogues and meta_data to pairs_meta 
                                                # meta_data = [row["work_id"], authors, row["rating"], row["category"], 
                                                #                 row["fandom"], row["relationship"], row["character"], 
                                                #                 row["additional tags"], row["language"], row["published"], 
                                                #                 row["status"], row["status date"], row["words"], row["chapters"], 
                                                #                 row["comments"], row["kudos"], row["bookmarks"], row["hits"], 
                                                #                 row["all_kudos"]]
                                                #modeled dialogue, response, and the rest of the data
                                                the_url = "https://archiveofourown.org/works/" + str(row["work_id"])
                                                
                                                #pairs_meta.append([num, dialogue1, dialogue2, the_url, hash(dialogue1 + dialogue2), pairs_count] + meta_data)
                                                #pairs_meta.append([num, dialogue1, dialogue2, the_url, hash(dialogue1 + dialogue2), pairs_count, row["work_id"]])
                                                pairs_meta.append([num, dialogue1, dialogue2, the_url, hash(dialogue1 + dialogue2), pairs_count, row["work_id"], row["title"],row["author"], row["fandom"], row["words"], row["category"]])
                                                num += 1
                                                break 
                                        else:
                                            in_between += 1 
                
                for i in pairs_meta:
                    if i[5] == row["work_id"]:
                        i[4] = pairs_count

                #num_pairs.append([int(row["words"].replace(",", "")), pairs_count])

            #clean up files
            os.remove(filename)
            os.remove(clean_text)

 

    return pairs, pairs_meta

# 22327
def create_csv(pairs, meta):

    csv_path = "dialogue-pairs.csv"
    metacsv_path = 'meta-pairs.csv'

    # write the key value pairs to the csv
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(pairs)
    
    print("CSV created successfully")

    # write the metadata to a csv
    with open(metacsv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(meta)
    
    print("Meta CSV created successfully")

    # create a excel file for both pages (just pairs and pairs + meta data)

    # creates dataframes from the 2D arrays
    df_pairs = pd.DataFrame(pairs[1:], columns=pairs[0])
    df_pairs_meta = pd.DataFrame(meta[1:], columns=meta[0])

    # write df's to an excel file
    # note: you can't generate an xlsx when the file is open b/c it needs to update. 
    with pd.ExcelWriter('dialogue-pairs.xlsx') as writer:
        df_pairs.to_excel(writer, sheet_name='Pairs', index=False)
        #df_pairs_meta.to_excel(writer, sheet_name='Pairs and Metadata', index=False)

    with pd.ExcelWriter('meta-pairs.xlsx') as writer:
        df_pairs_meta.to_excel(writer, sheet_name='Pairs and Metadata', index=False)

    print(".xlsx created successfully")


def main():

    body_path = "notmaturecorrect.csv" #work id, body 
    meta_path = "notmaturecorrect_meta.csv" #work id, url
    pairs, meta = get_pairs(body_path, meta_path)

    # for key in pairs:
    #     print(key, pairs[key])

    #create new csv
    create_csv(pairs, meta)
    print("CSV updated successfully")  

main()
