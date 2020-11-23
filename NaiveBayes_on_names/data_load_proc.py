
import warnings
warnings.simplefilter(action='ignore')

import re
import ftfy
import pandas as pd
from utils import *

class DIME():
    def __init__(self,filename):
        print(f'{timenow()}  -  load DIME')
        _ = self._load(filename)
        print(f'{filename} -- read {len(self.raw)} lines')
        _ = self._process()
        print(f'{filename} -- {len(self.df)} usable full names')
        print(f'{timenow()}  -  done')
        
    def _load(self,filename):
        self.raw = pd.read_csv(filename,header=1,
                 names=["raw","fname","ffname","mname","nname","lname","sourcetable"],
                 delimiter=';',dtype='str')

    def _process(self):

        dftmp = self.raw.fillna(' ')
        
        # take only ones with firstname
        dftmp2 = dftmp[(dftmp['fname']!=' ')]
        dftmp2.reset_index(inplace=True,drop=True)
        
        # concat all firstnames
        dftmp2['fname2'] = [[str(x)]+[str(y)]+[str(z)] 
                            for x,y,z in 
                            zip(dftmp2['fname'],dftmp2['mname'],dftmp2['nname']) ]

        # make sure lname is a string
        dftmp2['lname'] = [str(x) for x in dftmp2['lname']]
        
        # remove - 
        dftmp2['raw_lastname']=[[x.replace('-',' ')] for x in  dftmp2['lname']]
        dftmp2['raw_firstname']=[[x.replace("-"," ") for x in y] for y in dftmp2['fname2']]
        
        # split again
        dftmp2['raw_lastname']=[[x.split() for x in y] for y in dftmp2['raw_lastname']]
        dftmp2['raw_firstname']=[[x.split() for x in y] for y in dftmp2['raw_firstname']]
        
        
        #unnest lists
        dftmp2['raw_lastname']=[flat_list(x) for x in dftmp2['raw_lastname']]
        dftmp2['raw_firstname']=[flat_list(x) for x in dftmp2['raw_firstname']]

        #everything capitalize
        dftmp2['raw_lastname']=[[x.capitalize() for x in y] for y in dftmp2['raw_lastname']]
        dftmp2['raw_firstname']=[[x.capitalize() for x in y] for y in dftmp2['raw_firstname']]
        
        #make a total string for removing duplicates
        dftmp2['total']= [' '.join(x+y) for x,y in zip(dftmp2['raw_firstname'],dftmp2['raw_lastname'])]
        # remove dots
        dftmp2['total']= [x.replace('.','') for x in dftmp2['total']]
        
        self.df = dftmp2.drop(columns=  ['fname','fname2','lname','ffname','mname','nname','sourcetable'])

class WIPO_a():
    def __init__(self,filename):
        print(f'{timenow()}  -  load WIPO alpha')
        _ = self._load(filename)
        print(f'{filename} -- read {len(self.raw)} lines')
        _ = self._process()
        print(f'{filename} -- {len(self.df)} usable full names')
        print(f'{timenow()}  -  done')
    
    def _load(self,filename):
        self.raw = pd.read_csv(filename,header=None,names=['raw'],delimiter=';')
        
    def _process(self):
    
        # make sure it's a string
        self.raw['raw'] = [str(x) for x in self.raw['raw']]
        
        # split into lastname and firstnames
        self.raw['raw_lastname']=[x.split(',')[0].split() for x  in self.raw['raw']]
        self.raw['raw_firstname']=[x.split(',')[1:] for x  in self.raw['raw']]

        #remove commas and split again into list
        self.raw['raw_lastname']=[[x.replace(',',' ') for x in y] for y in self.raw['raw_lastname']]
        self.raw['raw_firstname']=[[x.replace(","," ") for x in y] for y in self.raw['raw_firstname']]
        
        #remove -
        self.raw['raw_lastname']=[[x.replace('-',' ') for x in y] for y in self.raw['raw_lastname']]
        self.raw['raw_firstname']=[[x.replace("-"," ") for x in y] for y in self.raw['raw_firstname']]
        
        # split again
        self.raw['raw_lastname']=[[x.split() for x in y] for y in self.raw['raw_lastname']]
        self.raw['raw_firstname']=[[x.split() for x in y] for y in self.raw['raw_firstname']]
        
        #unnest lists
        self.raw['raw_lastname']=[flat_list(x) for x in self.raw['raw_lastname']]
        self.raw['raw_firstname']=[flat_list(x) for x in self.raw['raw_firstname']]
        
        #everything capitalize
        self.raw['raw_lastname']=[[x.capitalize() for x in y] for y in self.raw['raw_lastname']]
        self.raw['raw_firstname']=[[x.capitalize() for x in y] for y in self.raw['raw_firstname']]
        
        #make a total string for removing duplicates
        self.raw['total']= [' '.join(x+y) for x,y in zip(self.raw['raw_firstname'],self.raw['raw_lastname'])]
        # remove dots
        self.raw['total']= [x.replace('.','') for x in self.raw['total']]
                
        self.df = self.raw
        
class ORCID():
    def __init__(self,filename_first,filename_last):
        print(f'{timenow()}  -  load ORCID')
        _ = self._load(filename_first,filename_last)
        print(f'{filename_first} + {filename_last} -- read {len(self.raw)} lines')
        _ = self._process()
        print(f'{filename_first} + {filename_last} -- {len(self.df)} usable full names')
        print(f'{timenow()}  -  done')
        

    def _load(self,filename_first,filename_last):
        rawlast = pd.read_csv(filename_last,header=None, names=["orcid",'lastname'],
                 delimiter=':',dtype='str')
        rawfirst = pd.read_csv(filename_first,header=None, names=["orcid",'firstname'],
                 delimiter=':',dtype='str')        

        self.raw=rawlast.merge(rawfirst,on='orcid',how='inner')

    def _process(self):

        df=pd.DataFrame({'raw':'',
                 'raw_lastname':[str(x) for x in self.raw['lastname']],
                 'raw_firstname':[str(x) for x in self.raw['firstname']]  })
        df['raw_lastname']=[x.split() for x in df['raw_lastname']]
        df['raw_lastname']=[[x.split('-') for x in y] for y in df['raw_lastname']]

        df['raw_firstname']=[x.split() for x in df['raw_firstname']]
        df['raw_firstname']=[[x.split('-') for x in y] for y in df['raw_firstname']]

        df['raw_firstname'] = [flat_list(x) for x in df['raw_firstname']]
        df['raw_lastname'] = [flat_list(x) for x in df['raw_lastname']]

        #everything capitalize
        df['raw_lastname']=[[x.capitalize() for x in y] for y in df['raw_lastname']]
        df['raw_firstname']=[[x.capitalize() for x in y] for y in df['raw_firstname']]
 
        #make a total string for removing duplicates
        df['total']= [' '.join(x+y) for x,y in \
                        zip(df['raw_firstname'],df['raw_lastname'])]
        # remove dots
        df['total']= [x.replace('.','') for x in df['total']] 

        self.df=df

class PMC():
    def __init__(self,filename):
        print(f'{timenow()}  -  load PMC')
        _ = self._load(filename)        
        print(f'{filename} -- read {len(self.raw)} lines')
        _ = self._process()
        print(f'{filename} -- {len(self.df)} usable full names')
        print(f'{timenow()}  -  done')

    def _load(self,filename):
        self.raw = pd.read_csv(filename,header=None,sep='|',names=["raw"],dtype='str')

        
    def _process(self):
        
        raw=self.raw
        ## make sure it's a string
        raw['fullproc']=[str(x) for x in raw['raw']]
        raw['fullproc']=[ftfy.fix_text(x) for x in raw['fullproc']]
        raw['raw_lastname']=[x.split(',')[0] for x in raw['fullproc']]
        raw['raw_firstname']=[' '.join(x.split(',')[1:]) for x in raw['fullproc']]
        raw['raw_firstname']=[x.replace('.',' ') for x in raw['raw_firstname']]
        raw['raw_firstname']=[x.split() for x in raw['raw_firstname']]
        raw['raw_firstname_initial']=[[x  for x in y if isinitial(x)==False] \
                                        for y in raw['raw_firstname']]
        raw['len_first']=[[len(x) for x in y] for y in raw['raw_firstname_initial']]
        raw['max_len_first'] = [max(x) if x else 0 for x in raw['len_first']]
        raw=raw[raw['max_len_first']>1]
        raw['raw_lastname']=[x.split() for x in raw['raw_lastname']]
        raw['raw_lastname']=[[x.split('-') for x in y] for y in raw['raw_lastname']]
        raw['raw_lastname']=[flat_list(x) for x in raw['raw_lastname']]
        
        df=raw[['raw','raw_lastname','raw_firstname']]
        
        #make a total string for removing duplicates
        df['total']= [' '.join(x+y) for x,y in \
                        zip(df['raw_firstname'],df['raw_lastname'])]
        # remove dots
        df['total']= [x.replace('.','') for x in df['total']] 
        
        self.df=df

    
class DBLP():
    def __init__(self):
        pass
    def _load(self):
        pass
    def _process(self):
        pass


