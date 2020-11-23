import pandas as pd
import numpy as np
from datetime import datetime

def print_infos(df_dime,df_orcid,df_wipo_a,dfall):
    print('ORCID total unique')
    print(len(df_orcid['total']),len(set(df_orcid['total'])))
    print('DIME total unique')
    print(len(df_dime['total']),len(set(df_dime['total'])))
    print('WIPO a total unique')
    print(len(df_wipo_a['total']),len(set(df_wipo_a['total'])))
    print('combined total unique')
    print(len(dfall['total']),len(set(dfall['total'])))
    
    
def isinitial(txt):
    # example:  A
    if len(txt)==1:
        return True
    # example:  A.
    if len(txt)==2:
        if txt[1]=='.':
            return True
    # example: AJ
    if len(txt)==2 or len(txt)==3:
        allupper = np.prod([x.isupper() for x in txt])
        if  allupper== 1:
            return True
        else:
            return False
    
    return False    

def flat_list(t):
    flat_list = [item for sublist in t for item in sublist]
    return flat_list

def timenow():
    return datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
