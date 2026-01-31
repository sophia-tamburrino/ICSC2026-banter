import os
import csv
import re
from openpyxl.workbook import Workbook
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import numpy as np
import random

# This file will go through notmaturecorrect.csv and notmaturecorrect_meta.csv to grab pairs of dialogue that match our requirements. 

# The get_pairs function takes the scraped data and metadata and goes through the dataframe line-by-line to pull a "dialogue" and "response".
# Notes: In order to be considered valid dialogue, it must have at least two double quotation marks (one to begin and one to end) within the line. 
# Additionally, to be considered a valid response to that dialogue, it must not be more than 2 lines ahead of it.
# Dependencies: Reads notmaturecorrect.csv and notmaturecorrect_meta.csv and outputs the pairs and pairs_meta lists.
# Arguments: body_path is the 'notmaturecorrect.csv' file, and meta_path is the 'notmaturecorrect_meta.csv' file. 

def get_pairs(body_path, meta_path):

    # create dialogue + meta data list
    pairs = [["Dialogue", "Response"]]
    pairs_meta = [["Number", "Dialogue", "Response", "URL", "hash", "num_pairs", "work_id", "title", "author", "fandom", "words","category"]]

    # save csv to a dataframe
    body_df = pd.read_csv(body_path, encoding="cp1252")
    meta_df = pd.read_csv(meta_path, header=None, names=['work_id', 'url'], encoding="cp1252")
    num = 1

    # iterate through each row (novel) in the csv
    for i, row in body_df.iterrows():

        id = row['work_id']
        dir = "body-text/"
        filename = dir + str(id) + "_body.txt"
        text = row["body"]  

        if not os.path.exists(dir):
            os.makedirs(dir)

        # save the text to a .txt file  
        with open(filename, "w") as w:
            w.write(str(text)) 

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
                    if (lines[index].strip().count("\"") >= 2):
                        dialogue1 = lines[index].strip()
                        temp_pairs.append(dialogue1)
                        # find the next possible line that has dialogue
                        # for use of counting the lines of writing in between dialouge
                        in_between = 0 
                        for i, line2 in enumerate(lines):
                            if (i > index) and (in_between < 3):
                                if lines[i].strip().count("\"") >= 2:
                                    dialogue2 = lines[i].strip()
                                    temp_pairs.append(dialogue2)
                                    pairs_count += 1
                                    pairs.append([dialogue1, dialogue2])
                    
                                    #modeled dialogue, response, and the rest of the data
                                    the_url = "https://archiveofourown.org/works/" + str(row["work_id"])
                                    pairs_meta.append([num, dialogue1, dialogue2, the_url, hash(dialogue1 + dialogue2), pairs_count, row["work_id"], row["title"],row["author"], row["fandom"], row["words"], row["category"]])
                                    num += 1
                                    break 
                                else:
                                    in_between += 1 

            for i in pairs_meta:
                if i[5] == row["work_id"]:
                    i[4] = pairs_count

        #clean up files
        os.remove(filename)
        os.remove(clean_text)

    return pairs, pairs_meta

# The create_csv function takes the pairs and pairs_meta lists from the above function and creates new CSVs for this data.
# Notes: This also creates Excel files to make them more readable.
# Dependencies: Reads the pairs and pairs_meta lists from the above function and creates the 'dialogue-pairs.csv' and 'meta-pairs.csv' functions. 
# Arguments: Pairs and meta from the returned lists in the above function.

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

    with pd.ExcelWriter('meta-pairs.xlsx') as writer:
        df_pairs_meta.to_excel(writer, sheet_name='Pairs and Metadata', index=False)

    print(".xlsx created successfully")

# The main function executes the get_pairs and create_csv methods, creating a final 'dialogue-pairs.csv' and 'meta-pairs.csv'.
# Dependencies: Reads the pairs and pairs_meta lists from the above function and creates the 'dialogue-pairs.csv' and 'meta-pairs.csv' functions. 
# Arguments: Pairs and meta from the returned lists in the above function.

def main():

    body_path = "notmaturecorrect.csv"
    meta_path = "notmaturecorrect_meta.csv"
    pairs, meta = get_pairs(body_path, meta_path)

    create_csv(pairs, meta)
    print("CSV updated successfully")  

main()
