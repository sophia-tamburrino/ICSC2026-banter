# This will generate a dataset consisting of 6,461 pairs of scraped dialogue from Archive of Our Own (AO3), with an emphasis on banter. 
# Note that because authors on AO3 may choose to either: a) delete their works or b) reserve them for logged-in AO3 users only at any given time, this number is subject to change. 
# We used this dataset for annotation geared towards banter identification, though our annotated dataset consisted of 7,440 pairs. 

import csv	
import hashlib
import re
import json

# using regular expressions, hash the given pair
def hash_pair(string1: str, string2: str) -> str:
	 combined_string = string1 + string2
	 # \W is equivalent to [^a-zA-Z0-9_] in Python's regex
	 cleaned_string = re.sub("\W", "", combined_string)
	 #return cleaned_string

	 h = hashlib.sha256()	 
	 # encode() necessary because hashlib sha256 takes bytes, not utf/ascii
	 h.update(cleaned_string.encode())

	 return '0x' + h.hexdigest() # returns string of hex digest

# get the ground truth 7440 annotations and convert the dialogue into a hashcode with associated banter label
# write hashtable to a file
def hash_ground_truth():
	GT = {}
	with open("./meta-pairs_fixed_VOTED_agreed_annotated_Zoe_Kinga.csv", mode ='r', encoding="utf8") as file:
		csvFileGT = csv.reader(file)

		for row in csvFileGT:
			key = hash_pair(row[1],row[2])
			value = row[0]
			if 'Banter' not in value:
				GT[key] = value
	

	with open('hash_ground_truth.json', 'w') as file:
		json.dump(GT, file)

def load_ground_truth():
	with open('hash_ground_truth.json', 'r') as file:
	 	hash_annotations = json.load(file)
	return hash_annotations

# Paper authors run this once to generate the hashed labels; you will not be able to run this
# because we are unable to make the csv on line 23 available on github due to it containing 
# dialogue from the novels
# hash_ground_truth()

hash_annotations = load_ground_truth()

# open the csv of all the dialogue downloaded from the novels
with open("./meta-pairs.csv", mode ='r', encoding="cp1252") as file:
	csvFileGT = csv.reader(file)

	dataset = []
	for row in csvFileGT:

		# if the hashed dialogue pair has an annotation, keep it
		if hash_pair(row[1], row[2]) in hash_annotations.keys():
			#print("found match")
			row.append(hash_annotations[hash_pair(row[1], row[2])])
			row[4] = hash_pair(row[1], row[2]) 
			row.pop(5)
			dataset.append(row)

file = open('./dataset_reproduction.csv', mode='w', newline='')
writer = csv.writer(file)
writer.writerow(['Number', 'Dialogue', 'Reponse', 'URL', 'hash', 'work_id', 'title', 'author', 'fandom', 'words', 'category', 'Banter'])

for line in dataset:
	writer.writerow(line)

file.close()