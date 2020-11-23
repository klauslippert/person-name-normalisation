There is **no automated pipeline** for creating the p values of the first and lastnames.

The steps to create your own p values are:

#### 1.  download the data-sets and do first processing manually

1.1.  **Pub Med Central** 
  -  make yourself familiar with and respect the Terms of Usage at https://www.ncbi.nlm.nih.gov/pmc/tools/openftlist/
  -  dowload as tar.gz from: https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/
  -  unpack the tar.gz files into folders named `folder_...`
  -  adopt and run `data/raw/extract_PMC_full-names.sh` 
  -  name the result `names_raw_PMC.csv` and put it into `data/raw/`

1.2.  **DIME**
  -  make yourself familiar with and respect the Terms of Usage at https://data.stanford.edu/dime
  -  download the full database as sqlite from: https://data.stanford.edu/dime  (at "data download links")
  -  use any sqlite-client to extract via `data/raw/extract_DIME_full-names.sql`
  -  name the result `names_raw_DIME.csv`  and put it into `data/raw/`

1.3.  **ORCID**
  -  make yourself familiar with and respect the Terms of Usage at https://orcid.org/content/orcid-public-data-file
  -  download the dump (only summaries needed) at: https://orcid.figshare.com/articles/dataset/ORCID_Public_Data_File_2020/13066970/1
  -  unpack 
  -  adopt and run `data/raw/extract_ORCID_first-names.sh` and `data/raw/extract_ORCID_last-names.shh`
  -  name the results `names_first_raw_ORCID.csv` and `names_last_raw_ORCID.csv` and put it into `data/raw/`

#### 2. adopt and run `main.py` 
for further processing and creation of the p-values. data will be stored in `data/proc/` 

#### 3. result will be placed into `data/result/`
this resulting pickle file `p_firstname.p` will be downloaded from the library. You can replace it with your own pickled creation.

```
p_firstname = {                       # <class dict>
               'name1': p-value1,     # names are the keys
               'name2': p-value2,     # values are the p values for name being a firstname
               ...
               }
               
pickle.dump( p_firstname, open( "data/result/p_firstname.p", "wb" ) )     # pickle this dict
              
```






