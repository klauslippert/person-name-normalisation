import pandas as pd
from data_load_proc import *
import pickle
from utils import *
from collections import Counter

def save_to_disc(df,name):
    print(f'{timenow()}  -  saving to disc')    
    pickle.dump(df,open(name,"wb"))
    print(f'{timenow()}  -  done')
    

#df_wipo_a = WIPO_a('data/raw/names_raw_WIPOalpha.csv').df
#_=save_to_disc(df_wipo_a,"data/proc/df_wipo_a.p")

#df_dime   = DIME('data/raw/names_raw_DIME.csv').df
#_=save_to_disc(df_dime,"data/proc/df_dime.p")

#df_orcid  = ORCID('data/raw/names_first_raw_ORCID.csv','data/raw/names_last_raw_ORCID.csv').df
#_=save_to_disc(df_orcid,"data/proc/df_orcid.p")

#df_pmc = PMC('data/raw/names_raw_PMC.csv').df
#_=save_to_disc(df_pmc,"data/proc/df_pmc.p")



df_dime   = pickle.load(open("data/proc/df_dime.p","rb"))
#df_wipo_a = pickle.load(open("data/proc/df_wipo_a.p","rb"))
df_orcid  = pickle.load(open("data/proc/df_orcid.p","rb"))
df_pmc    = pickle.load(open("data/proc/df_pmc.p","rb"))

## concat
print(f'{timenow()}  -  concat all datasets')
dfall=pd.concat([df_dime,df_orcid,df_pmc])
print(f'{timenow()}  -  done  ->  {len(dfall)} usable names')

## remove umlaute
def replace_umlaute(txt):
    umlaute = {'ä':'ae','ö':'oe','ü':'ue',
               'Ä':'Ae','Ö':'Oe','Ü':'Ue',
               'ß':'ss'}
    for umlaut in umlaute.keys():
        txt = txt.replace(umlaut,umlaute[umlaut])
    return txt
dfall['total'] = [replace_umlaute(x) for x in dfall['total']]

#legacy
#_ = print_infos(df_dime,df_orcid,df_wipo_a,dfall)

## remove doubles
print(f'{timenow()}  -  removing doubles')
dfall=dfall.drop_duplicates(subset=['total'], keep='first')
print(f'{timenow()}  -  done  ->  {len(dfall)} usable unique names')

## subset for development
#pickle.dump(dfall[:10000],open("dfall_small.p","wb"))
#dfall   = pickle.load(open("dfall_small.p","rb"))

print(f'{timenow()}  -  calc p values')
dfall['firstname']=[[x for x in y if isinitial(x) is False] \
                        for y in dfall['raw_firstname'] ]

list_last  = [item.lower() for sublist in dfall['raw_lastname'].to_list() for item in sublist]
list_first = [item.lower() for sublist in dfall['firstname'].to_list() for item in sublist]

## remove umlaute
list_last  = [replace_umlaute(x) for x in list_last]
list_first = [replace_umlaute(x) for x in list_first]

## count
dict_lastnames  = Counter(list_last)
dict_firstnames = Counter(list_first)

lastnames  = list(set(list_last))
firstnames = list(set(list_first))
allnames   = list(set(firstnames+lastnames))

p_firstname = dict(zip(allnames,
    [dict_firstnames[x]/(dict_firstnames[x]+dict_lastnames[x]) for x in allnames] ) )
p_lastname = dict(zip(allnames,
    [dict_lastnames[x]/(dict_firstnames[x]+dict_lastnames[x]) for x in allnames] ))

print(f'{timenow()}  -  done')
print(f'p-values for {len(firstnames)} unique firstnames and {len(lastnames)} unique lastnames => {len(allnames)} unique names in total.')


print(f'{timenow()}  -  saving to disc')
pickle.dump( p_firstname, open( "data/result/p_firstname.p", "wb" ) )
pickle.dump( p_lastname, open( "data/result/p_lastname.p", "wb" ) )
print(f'{timenow()}  -  done     p_firstname.p  +  p_lastname.p')


print('bye')
