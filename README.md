# ICSC-banter-classifier

This is a tutorial on how to generate a dataset consisting of 6,461 pairs of scraped dialogue from Archive of Our Own (AO3), with an emphasis on banter. Note that because authors on AO3 may choose to either: a) delete their works or b) reserve them for logged-in AO3 users only at any given time, this number is subject to change. We used this dataset for annotation geared towards banter identification, though our annotated dataset consisted of 7,440 pairs. Additionally, some novels will yield HTTP 525 errors unpredictably.


### Scraping Fanfiction Text 
We utilized code from @/radiolarian & @/ssterman's [AO3Scraper](https://github.com/radiolarian/AO3Scraper) to scrape fanfiction from AO3 under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) license.
* Said code includes the following programs: ao3_work_ids.py and csv_to_txts.py
  
For our project, we ran this program with the following commands: 
1. Ensure that all dependencies are installed, run: `pip install -r classifier_dependencies.txt`


2. Run: `python ao3_work_ids.py "https://archiveofourown.org/works?commit=Sort+and+Filter&work_search%5Bsort_column%5D=kudos_count&work_search%5Bother_tag_names%5D=Banter&exclude_work_search%5Brating_ids%5D%5B%5D=12&exclude_work_search%5Brating_ids%5D%5B%5D=9&exclude_work_search%5Brating_ids%5D%5B%5D=13&work_search%5Bexcluded_tag_names%5D=Rape%2FNon-Con&work_search%5Bcrossover%5D=&work_search%5Bcomplete%5D=&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bquery%5D=&work_search%5Blanguage_id%5D=&tag_id=Banter" --num_to_retrieve 100 --out_csv notmaturecorrect_meta --header "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0"`  

This make take around 5-10 minutes.

This will return **notmaturecorrect_meta.csv**, which has the work IDs of 100 of the most kudosed fanfics with the 'Banter' tag, that are also rated for 'General Audiences' or 'Teen and Up'. 

3. Run `python url_grabber_meta.py`. This might take a while (~35-40 min). Note: Not all fics have a defined 'category', so the 'category' cells will be empty for a few of them. So, if you see something like "Unable to extract category 'NoneType' object has no attribute 'find_all'", no need to be alarmed, the scraper is working as it should!

This will return **notmaturecorrect.csv**, which contains the work IDs, scraped body texts, and other metadata (author, wordcount, title, fandom, & category) of the fanfiction identified in the previous step. 

---
### Extracting Dialogue Pairs for Annotation 

1. Run `python all_rows_generator.py`. This will extract all the dialogue pairs from the novels mined above.

This will return **meta-pairs.csv**, which contains the work IDs, scraped body texts, and other metadata (author, wordcount, title, fandom, & category) of the fanfiction identified in the previous step. 

2. Run `python reproduce_dataset.py`. This will connect the banter labels in `hash_ground_truth.json` with any row in `meta-pairs.csv` that has such an annotation.

All dialogue pairs from the novels mined above for which there existed a banter annotation can now be found in **dataset_reproduction.csv**, which includes the metadata downloaded as well. 
