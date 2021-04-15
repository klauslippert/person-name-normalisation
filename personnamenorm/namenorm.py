from ftfy import fix_text
from nltk import word_tokenize as wt
import logging
import pickle
from numpy import prod
import os
import re

# logging
logger = logging.getLogger(__name__)


class namenorm():
    '''
    unifying different notations of person names
    detect / extract titles and prefixes
    '''
    
    def __init__ (self,debug=False):
        ''' init namenorm:  logging handling
           
            inp: flag for debug-level DEBUG
            upd: self.debug        <bool>
                 self.p_firstname  <dict> | p values from Naive Bayes
                 self.dict_allg    <dict> | annotation dict for prefix an titles
            out: None
        '''    
        
        
        ''' 2DO      
            #    notest           remove et.al
            #    notest           appendix: Jr. / Sen.
            #      test 034, 035  d'Last -> d' Last
            #                     capitalize every word in every prefix

   
              
              
        '''
        #print('debug here')
        
        self.debug = debug
        
        # handle logging
        if logger.hasHandlers():        # there is already logging
            logger.addHandler(logging.NullHandler())
        else:                           # no logging until now
            ch=logging.StreamHandler()
            ch.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s') )
            logger.addHandler(ch)

        # set log level for this module
        if self.debug:   
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.WARNING)

        # load p values from Naive Bayes
        
        path=os.path.dirname(os.path.abspath(__file__))
        #print(path)
        self.p_firstname = pickle.load(open(path+"/p_firstname.p","rb"))
        logger.debug('loaded p values firstname')

        # annotation dict
        _ = self._create_dict_lookup()

        # a prefix before a word makes it more likely to be a lastname
        # this factor is multplied by p_firstname if the word has a prefix
        self.prefix_faktor=0.8
        
        # if there is NO comma inside it's more likely to be: firstname lastname 
        # (factor on p_firstname of the first word , factor on p_firstname of the last word)
        # this is applied only to the first and the last word 
        #self.fl_faktor=(1.1,0.9)
        self.fl_faktor=(1,1)
        
        # if there is a comma inside it's more likely to be: lastname firstname
        # (factor on p_firstname of the first word , factor on p_firstname of the last word)
        # this is applied only to the first and the last word 
        #self.lf_faktor=(0.9,1.1)
        self.lf_faktor=(1,1)
        
        return None
    
    def unify(self,raw):
        ''' complete pipeline for unifying names
        
            inp: raw <str>  |   
            upd: 
            out: None
        '''    

        # check type of input
        if isinstance(raw,str) == False:
            logger.critical("Input must be <class 'str'>, you gave me "+str(type(raw)))
            return
        else:
            logger.debug(f'input OK {str(type(raw))}')
        
        # create empty results
        self.name={
                   'raw':raw,
                   'firstname':[],
                   'lastname':[],
                   'title':[],
                   'fullname':'',
                   'fullname_abbrev':''
                  }

        # text processing
        self.__text = self.name['raw']
        
        logger.debug('input:')
        logger.debug(f'    "{self.__text}"')
        
        _ = self._fix_unicode()
        _ = self._remove_formating_chars()
        _ = self._remove_special_characters()
        
        
        #self.__text = self.__text.replace('.','. ')
        #logger.debug("replace '.' by '. '")
        #logger.debug(f'    "{self.__text}"')
        
        
        _ = self._replace_umlaute()
        _ = self._remove_multiple_whitespace()
        self.__text = ' '+self.__text+' '
        _ = self._transform_prefixes()
        
        # extraction
        
        _ = self._tokenize_annotate(0)
        _ = self._extract_title()
        _ = self._remove_bracket_content()
        _ = self._cut_CamelCase()   
        
        _ = self._tokenize_annotate(0)
        
        _ = self._cut_initials()
        _ = self._tokenize_annotate(2)
        
        
        version = 2
        if version == 1:  # old version
            _ = self._extract_name()
            _ = self._extract_prefix()
            
        else:  #latest version
            self.name['prefix']=''
            _ = self.pre_core()
            if len(self.sent)==0:
                return
            result = self.core()
            
            
            
            ## remove _ in first and lastname
            firstname = [x[0] for x in result if x[4]=='first']
            firstname = [x.replace('_',' ') for x  in firstname]

            lastname = [x[0] for x in result if x[4]=='last']            
            lastname = [x.replace('_',' ') for x  in lastname]
            
            self.name['firstname']= firstname 
            self.name['lastname']= lastname
            
                
        
        
        # clean up results
        _ = self._capitalize()
        _ = self._create_output()

        
        
        
        
        ## put together prefix and next str
        
        ## after (the last)  initial, there must be a cut
        ## index of last occurence
        #li=[x[1] for x in sent]
        
        #cutidx = len(li) - 1 - li[::-1].index('initial')
        #logger.debug(str(cutidx))
#        if cutidx==len(li):  # kein cut, aber zumind zweiter teil ist firstname
#            cut=None
#            ctrl='lf'
#        else:                # cut gefunden, erster teil ist firstname
#            cut=cutidx
#            ctrl='fl'
# 
#        if cut is None: #search the cut
#            res=[]
#            for c in range(1,len(li)):
                
        
        
            
                

        
    def _fix_unicode(self):    
        ''' fix bad unicode with ftfy 
            https://pypi.org/project/ftfy/
            
            inp: self.text <str> | text            
            upd: self.text <str> | clean unicode text
            out: None
        '''
        self.__text = fix_text(self.__text)
        
        logger.debug('fixed unicode:')
        logger.debug(f'    "{self.__text}"')
        return None
        
    def _remove_formating_chars(self):
        ''' remove 
            * tabs \t
            * everything which comes after newline \n or ¶
            
            inp: self.text  <str> | text
            upd: self.text  <str> | text without formating chars
            out: None
        '''
        self.__text = self.__text.replace('\n','CUT')
        self.__text = self.__text.replace('¶','CUT')
        self.__text = self.__text.split('CUT')[0].strip()
        self.__text = self.__text.replace('\t',' ')            
        
        logger.debug('removed formating characters:')
        logger.debug(f'    "{self.__text}"')
        return None

    def _remove_special_characters(self):
        ''' remove special characters
   
            inp: self.text  <str> | text
            upd: self.text  <str> | text without special chars       
            out: None
        '''
        special_chars='!§%&/=<>;:_$?*+#|'   #-
        for char in special_chars:
            self.__text=self.__text.replace(char,' ')
        very_special_chars='\\'
        for char in very_special_chars:        
           self.__text=self.__text.replace(char,' ')
       
       
       
        ## remove '-' if next character is ' '
        while 1==1:
            try:
                idx = self.__text.index('-')
                if idx < len(self.__text) and self.__text[idx+1]==' ':
                    self.__text=self.__text[:idx] + ' ' + self.__text[idx + 1:]
                else:
                    self.__text=self.__text[:idx] + '_' + self.__text[idx + 1:]
            except:
                break
        self.__text = self.__text.replace('_','-')
       
       
        ## some special prefix
        self.__text=self.__text.replace("'","_ ")
       
       
       
        logger.debug('removed special characters:')
        logger.debug(f'    "{self.__text}"')
        return None


    def _remove_multiple_whitespace(self):
        ''' reducing multiple withespaces to one whitespace
            + leading and trailing whitespaces
   
            inp: self.text  <str> | text
            upd: self.text  <str> | text with single whitespaces
            out: None
       '''
        self.__text = ' '.join(self.__text.split()).strip()
        
        logger.debug('removed multiple whitespace:')
        logger.debug(f'    "{self.__text}"')
        return None

    def _replace_umlaute(self):
        ''' replace german Umlaute
   
            inp: self.text  <str> | text
            upd: self.text  <str> | text without Umlaute
            out: None
       '''
        umlaute = {'ä':'ae','ö':'oe','ü':'ue',
                   'Ä':'Ae','Ö':'Oe','Ü':'Ue',
                   'ß':'ss'}
        for umlaut in umlaute.keys():
            self.__text = self.__text.replace(umlaut,umlaute[umlaut])
            
        logger.debug('replaced Umlaute:')    
        logger.debug(f'    "{self.__text}"')
        return None

    def _tokenize_annotate(self,run):
        ''' tokenize text (using nltk tokenizer)
            and annotate text (using lookup dict) 
        
            inp: self.__text           <str> | text
                 self.dict_allg     <dict> | lookup dictionary
            upd: self.sentence <list(str)> | tokenized text
                 self.annotate <list(str)> | annotations
            out: None
        '''

        logger.debug('tokenize')
        self.__sentence=wt(self.__text)
        #self.__sentence=self.__text.split(' ')
        logger.debug(f'    {self.__sentence}')
        
        
        
        self.__annotate=[]
        for word in self.__sentence:
            if word.isnumeric():
                self.__annotate.append('zahl')
            else:
                try:
                    self.__annotate.append(self.__dict_allg[word])
                except:
                    if (len(word)==1) or \
                       (len(word)==2 and word[1]=='.') or \
                       (word.lower()=='jr') or \
                       (word.lower()=='jr.') :
                        self.__annotate.append('initial')
                    else:
                        self.__annotate.append('str')
        
        
        self.__p_first = [self._get_p_word(x)\
                          if y=='str' or y=='initial'\
                          else (1,1)\
                          for x,y in zip(self.__sentence,self.__annotate )\
                          ]
        
        # in the second run, remove dots
        #if run==2:
        #    self.__sentence = [x.replace('.',' ') for x in self.__sentence]
            


        logger.debug('lookup p values')
        return None

    def _create_dict_lookup(self):
        ''' lookup dictionaries for extracting 
            punctuations, titles, prefixes
            
            inp:  None
            upd: self.dict_allg  <dict> |  one lookup dictionary
            out: None
        '''
        # punctuations
        dict_allg = ({'(':'klammerauf',')':'klammerzu',
                      '[':'klammerauf',']':'klammerzu',
                      '{':'klammerauf','}':'klammerzu',
                      ',':'komma',
                      '.':'punkt'
                      })

        # titles
        list_title = ['Prof.','Prof',
                      'PhD', 'Ph.D.','Ph. D.','Ph. D', 'Dr.','Dr',
                      'MBA','MSc.','BSc.','M.A.','B.A.',
                      'MSc','BSc',#'M.A','B.A',
                      'Dipl.','Dipl',
                      'Dipl. Ing.','Dr. Ing.','Dipl. Ing','Dr. Ing']

        list_title = list_title +\
                     [x.upper() for x in list_title] +\
                     [x.lower() for x in list_title] +\
                     [x.capitalize() for x in list_title]
        
                 
        dict_title = dict(zip(list_title, ['titel']*len(list_title)))

        # name prefixes
        #  german, french, italian, dutch
        #  spanish, portuguese MISSING
        prefix_list = ['von und zu','von dem','von der','von',
                       'zu','vom','zum', 'van der',
                       'de',"d_",'le','la','de la',
                       'di','de','del','da','degli','dalla',
                       'van de','van ter','van','ter',
                       'van den', 'van der', 'te','o_','van dan','van den', 'van der', 'abu'
                      ]
        
        prefix_list = prefix_list +\
                      [x.upper() for x in prefix_list] +\
                      [x.lower() for x in prefix_list] +\
                      [x.capitalize() for x in prefix_list]
        
        prefix_list_sort = sorted(prefix_list,key=len,reverse=False)
        prefix_list_space = prefix_list_sort
        prefix_list_underscore = ['_'.join(x.split()) for x in prefix_list_space]
        
        self.__prefix_list_space = prefix_list_space
        self.__prefix_list_underscore = prefix_list_underscore
        
        
        dict_prefix = dict(zip(prefix_list_underscore,\
                               ['prefix']*len(prefix_list_underscore)))

        _ = dict_allg.update(dict_title)
        _ = dict_allg.update(dict_prefix)

    
        self.__dict_allg = dict_allg
        self.annotation_dict = dict_allg
        
        logger.debug('created lookup dictionary')
        return None
    
    def _remove_bracket_content(self):
        '''remove anything inside any brackets and the brackets
           
           inp: self.sentence <list(str)> | tokenized text
                self.annotate <list(str)> | annotations
           upd: self.sentence <list(str)> | tokenized text without brackets and content
                self.annotate <list(str)> | annotations without brackets and content
           out: None
        '''
        while 1==1:
            try:
                von = self.__annotate.index('klammerauf')
                bis = self.__annotate.index('klammerzu')
                self.__annotate[von:bis+1]=''
                self.__sentence[von:bis+1]=''
            except:
                break
            
        logger.debug('removed bracket content:')
        logger.debug(f'    {self.__sentence}')
        
        return None            
            
        
    def _transform_prefixes(self):
        ''' transforms prefixes in text
            for extracting them correctly
            by replacing spaces with underscore
            
            inp: self.__prefix_list_space      <list(str)> | list of prefixes with spaces
            upd: self.__prefix_list_underscore <list(str)> | list of prefixes with underscore
            out: None
        '''
        for x,y in zip(self.__prefix_list_space, self.__prefix_list_underscore):
            self.__text=self.__text.replace(' '+x+' ',' '+y+' ')
        
        logger.debug('transformed prefixes')
        logger.debug(f'    "{self.__text}"')
        return None
    
    def _extract_title(self):   
        ''' extract the educational titles
            
            inp: self.__sentence    <list(str)> | tokenized string
                 self.__annotate    <list(str)> | annotations
            upd: self.name['title'] <list(str)> 
            out: None
        '''
        self.name['title'] = [x for x,y in zip(self.__sentence,self.__annotate) if y == 'titel']
        
        logger.debug('extracted titles:')
        logger.debug(f"    name['title']:{self.name['title']}")
        return None
    
    def _extract_prefix(self):   
        ''' extract the prefix
            
            inp: self.__sentence     <list(str)> | tokenized string
                 self.__annotate     <list(str)> | annotations
            upd: self.name['prefix'] <list(str)>
            out: None
        '''
        self.name['prefix'] = [x for x,y in zip(self.__sentence,self.__annotate) if y == 'prefix']   
        self.name['prefix'] = [x.replace('_',' ') for x in self.name['prefix']]
        #self.name['prefix'] = [[' '.join([x.capitalize() for x in y]) for y.split() in z] for z in self.name['prefix']]
        try: 
            idx=self.name['prefix'].index('d ')
            self.name['prefix'][idx]="d'"
        except:
            pass
        
        logger.debug('extracted prefix:')
        logger.debug(f"    name['prefix']:{self.name['prefix']}")
        return None
    
    def _cut_CamelCase(self):
        '''cut CamelCase words into multiple words
           only annotation <str>, not <prefix>, not <title>
           
           inp: self.__sentence <list(str)> | tokenized text
                self.__annotate <list(str)> | annotations
           upd: self.__text <str>           | text without CamelCase
           out: None
        '''
        def CamelCase_one_word(word):
            if word.isupper():     ## total upper case -> do nothing
                return word
            elif word.islower():   ## total lower case -> do nothing
                return word
            else:                  ## mixed upper and lower case -> cut
                uppercase = [True if x.isupper() else False for x in word ]
                indices=[ii for ii,x in enumerate(uppercase) if x]
                res = ' '.join([word[i:j].strip() for i,j in zip(indices, indices[1:]+[None])])
                ## do not destroy double names with minus in between
                if len(res.split())>1 and res.split()[0][-1]=='-':
                    res = res.replace(' ','')
                return res
            
      
        self.__text = ' '.join([CamelCase_one_word(x) if y == 'str' else x for x,y in\
                                 zip(self.__sentence,self.__annotate)])
        
        logger.debug('cut pure CamelCase:')
        logger.debug(f'    {self.__text}')
        
    def _cut_initials(self):        
        ## cut initials that are put together , e.g. A.J.
        ## tokenizer does split the last dot away => A.J
        def split_initials_one_word(word):
            if len(re.findall("^[A-Z]\.[A-Z]$",word))==1:
                return word[0]+' '+word[2]
            else: 
                pass
            return word

        self.__text = ' '.join([split_initials_one_word(x) if y == 'str' else x for x,y in\
                                 zip(self.__sentence,self.__annotate)])
        
        logger.debug('cut concat with dot Initials:')
        logger.debug(f'    {self.__text}')           
        
        
        
        
        return None        


    def _get_p_word(self,origword):
        wordlist = origword.split('-')
        a=[]
        b=[]

            
        for word in wordlist:
            try:
                a.append(self.p_firstname[word.lower()])
                b.append(1-a[-1])
            except:
                a.append(0.5)
                b.append(0.5)
                logger.info(f'name "{word}" is unknown -> p=0.5')
                
        amax=max(a)
        bmax=max(b)
        abmax=max(amax,bmax)
        if amax==abmax:
            atotal=amax
            btotal=1-amax
        
        else:
            atotal=1-bmax
            btotal=bmax
#            if len(wordlist)>1:
#                logger.debug(f'    found double name: {origword} and assigned p(firstname)')        

        if len(wordlist)>1:
            logger.debug(f'    found double name: {origword} with p(firstname):{a} and assigned p(firstname)={atotal}')            
        
        return atotal,btotal
        
        
    def _get_p(self,namelist):
        '''decide according to the total p-value of a string of words,
           which combination of first- / lastnames is the most likely
           
           inp: namelist <list(str)>  | list of words 
           upd: 
           out: firstname <list(str)> | list of firstnames, same order as input
                lastname  <list(str)> | list of lastnames,  same order as input
        '''
        ## LEGACY: still not decided how to deal with double names with minus in between
        ## right now: minus is removed with other special characters and names are treated 
        ## seperately
        
        ## minus in between names:
        ## already in the dict? -> do nothing
        ## not: add the max p-value of the single names to the dict
        #for x in namelist:
        #    y=x.split('-')
        #    if len(y)>1:
        #        try:
        #            print('huhu1')
        #            _=self.p_firstname[x]
        #        except:
        #            print('huhu2')
        #            a=[]
        #            for i in y:
        #                try:
        #                    a.append(self.p_firstname[i])
        #                except:
        #                    a.append(0.5)
        #            print(a)
        #            self.p_firstname[x]=prod(a)
        #        print(self.p_firstname[x])

        ## go on                
        p_first=[]
        p_last=[]
    
        for x in namelist:
            try:
                a=self.p_firstname[x.lower()]
                b=1-a
            except:
                a=0.5
                b=0.5
        
            # abbrev must be firstnames
            if len(x)==1:
                a=1
                b=0
        
            if a==0:
                a=1e-4
        
            if b==0:
                b=1e-4
               
            p_first.append(a)
            p_last.append(b)
    
        cutidxlist = range(1,len(namelist))
    
        plist_fl=[]
        plist_lf=[]
        for cutidx in cutidxlist:
            plist_fl.append(prod(p_first[0:cutidx]+p_last[cutidx:]))
            plist_lf.append(prod(p_last[0:cutidx]+p_first[cutidx:]))
            #print(prod(p_first[0:cutidx]+p_last[cutidx:]),prod(p_last[0:cutidx]+p_first[cutidx:]))
        #print(plist_fl)
        #print(plist_lf)
        cutat_fl=plist_fl.index(max(plist_fl))
        cutat_lf=plist_lf.index(max(plist_lf))
    
        if max(plist_fl)>=max(plist_lf):
            cutat=cutat_fl
            firstname=namelist[0:cutat+1]
            lastname=namelist[cutat+1:]
        else:
            cutat=cutat_lf
            lastname=namelist[0:cutat+1]
            firstname=namelist[cutat+1:]
    
        logger.debug('version 1: got p-values for list of words')
        return firstname, lastname


    #def _extract_name(self):
        #''' extract the first and the last names
            
            #inp: self.__sentence  <list(str)>        | tokenized string
                 #self.__annotate  <list(str)>        | annotations
            #upd: self.name['firstname'] <list(str)>  | firstnames, same order as input
                 #self.name['lastname']  <list(str)>  | lastnames,  same order as input
            #out: None
        #'''
        ### is there a comma ?
        #try:
            #idx=self.__annotate.index('komma')
            
        #except: 
            #idx=-1
            

        ### gather first and last names (both plural)
        #firstname= []
        #lastname=[]

        ### case 1:  lastnames comma firstnames
        #######################################
        #if idx>-1:    
            #vorkomma_sentence = self.__sentence[:idx]
            #vorkomma_annotate = self.__annotate[:idx]
            #nachkomma_sentence = self.__sentence[idx+1:]
            #nachkomma_annotate = self.__annotate[idx+1:]
    
            ## extract lastnames -> before comma
            #while 1==1:
                #try:
                    #idx2 = vorkomma_annotate.index('str')
                    #lastname.append(vorkomma_sentence[idx2])
                    #vorkomma_annotate[idx2]=''
                #except:
                    #break
                    
            ## extract firstnames -> after comma
            #while 1==1:
                #try:
                    #idx2 = nachkomma_annotate.index('str')
                    #firstname.append(nachkomma_sentence[idx2])
                    #nachkomma_annotate[idx2]=''
                #except:
                    #break
            
            #if len(lastname)==0:
                #lastname=firstname
                #firstname=[]
            
        ### case 2:  firstnames lastnames or lastnames firstnames
        #######################################
        #else:   
            #allwords=[x    for x,y in zip(self.__sentence,self.__annotate) if y=='str']
            
            #allwords=[x.replace('.','') for x in allwords]
            
            #if len(allwords)==0:
                #self.name['firstname']=[]
                #self.name['lastname']=[]
                #return
            #elif len(allwords)==1:
                #self.name['firstname']=[]
                #self.name['lastname']=allwords
                #return

            ## LEGACY: hard coded rule based        
            ##lastname = [allwords[-1]]
            ##firstname = allwords[:-1]
        
            #firstname, lastname = self._get_p(allwords)
        
        
        #self.name['firstname'] = firstname
        #self.name['lastname']  = lastname
        
        #logger.debug('Version 1: extract name')
        #return None
  
    def _cap_all(self,namelist):
        
        name=[]
        for word in namelist:
            a=word.split()
            c=[]
            for word2 in a:
                b=word2.split('-')
                c.append('-'.join([x.capitalize() for x in b]))
            
            #name2=[]
            #for word2 in a.split('-'):
            #    name2.append('-'.join([x.capitalize() for x in a]))    
            
            
            name.append(c)
        
        res = [' '.join(x) for x in name]
        ##[item for sublist in name for item in sublist]
        
        logger.debug(f'    ... capitalized: {namelist}  ->  {res}')
        return res
  
  
  
    def _capitalize(self):
        ''' capitalize First and Lastnames
        
            inp: self.name <dict> | resulting dict  
            upd: self.name <dict> | resulting dict
            out: None
        '''
        
        logger.debug('firstname ...')
        self.name['firstname'] = self._cap_all(self.name['firstname'])
        logger.debug('lastname ...')
        self.name['lastname'] = self._cap_all(self.name['lastname'])
        
        return None
    
    def _create_output(self):
        ''' create fullnames as standardised output
            lower case prefix
            
            inp: self.name            <dict> | resulting dict
            upd: self.fullname         <str> | (prefix) last, first .. not titles
                 self.fullname_abbrev  <str> | (prefix) last, initials .. not titles   
                 self.prefix           <str> | prefix in lower case
            out: None
        '''
        self.name['prefix'] = [x.lower() for x in self.name['prefix']]
                               
        self.name['fullname'] = '{}, {}'.format(  #' '.join(self.name['prefix']),
                                           ' '.join(self.name['lastname']),
                                           ' '.join(self.name['firstname'])
                                           ).strip()
        
        # TODO this has to be more general
        self.name['fullname'] = self.name['fullname'].replace("d' ","d'")
        
        
        self.name['fullname_abbrev'] = '{}, {}'.format(    #      ' '.join(self.name['prefix']),
                                                  ' '.join(self.name['lastname']),
                                                  ' '.join([x[0] for x in self.name['firstname']])        
                                         ).strip()
        self.name['fullname_abbrev'] = self.name['fullname_abbrev'].replace("d' ","d'")
        
        
        
        
        if self.name['fullname']==',':
            self.name['fullname']=''
            self.name['fullname_abbrev']=''

        logger.debug('created formated output:')
        logger.debug(f"    name['fullname']:'{self.name['fullname']}'")
        logger.debug(f"    name['fullname_abbrev']:'{self.name['fullname_abbrev']}'")
        return None
            
######################    
#### LEGACY STUFF ####
######################
    
    #def _remove_minus(self):
    #    self.__text=self.__text.replace('-',' ')
## legycy until here


    def pre_core(self):
        self.sentence=[[x,y,z[0],z[1],None] for x, y,z in \
                    zip(self.__sentence,self.__annotate,self.__p_first )]
        logger.debug(f'        {self.sentence}')
        self.sent=[x for x in self.sentence if x[1] in ['prefix','initial','str','komma']]
        #self.sent=[x for x in self.sentence if x[1] in ['prefix','initial','str']]
        
        #logger.debug(f'        {self.sentence}')
        logger.debug('Version 2: extract names')
        logger.debug('    data: <list of lists>: [ "word","annotation",p(firstname),p(lastname),"mapping" ]')
        logger.debug(f'        {self.sent}')
        return None

    def core(self):
        
        
        

        ### is there a comma inside?
        if 'komma' in [x[1] for x in self.sent]:
            self.komma_inside=True
        else:            
            self.komma_inside=False
        
        
        # apply factors 
        if self.komma_inside:
            ## names without comma are more likely to be firstname lastname   
            ## apply on p_firstname
            self.sent[0][2]  = self.sent[0][2]*self.fl_faktor[0]
            self.sent[-1][2] = self.sent[-1][2]*self.fl_faktor[1]
            ## adjust p_lastname
            self.sent[0][3]  = 1-self.sent[0][2]
            self.sent[-1][3] = 1-self.sent[-1][2]
        else:
            ## names with comma are more likely to be more lastname firstname
            ## apply on p_firstname            
            self.sent[0][2]  = self.sent[0][2]*self.lf_faktor[0]
            self.sent[-1][2] = self.sent[-1][2]*self.lf_faktor[1]
            ## adjust p_lastname
            self.sent[0][3]  = 1-self.sent[0][2]
            self.sent[-1][3] = 1-self.sent[-1][2]
            
        sent=self.sent
        
        # is there a prefix inside ?
        flag_prefix_end = False
        if 'prefix' in [x[1] for x in sent]:
            logger.debug('    prefix found')
            
            ## position prefix not at the end
            if 'prefix' in [x[1] for x in sent[:-1]]:    
                ## concat prefix with the next str
                while 'prefix' in [x[1] for x in sent[:-1]]:
                    ## wo ist der prefix?
                    idx = [x[1] for x in sent[:-1]].index('prefix')
                    sent[idx][1]=None
                    sent[idx+1][0]=sent[idx][0]+'_'+sent[idx+1][0]
                    ## prefix is more likely with lastname
                    sent[idx+1][2]=sent[idx+1][2]*self.prefix_faktor   # reduce p firstname
                    sent[idx+1][3]=1-sent[idx+1][2]     # adopt to p lastname
                sent=[x for x in sent if x[1] != None]
                logger.debug(f'        concat prefix with the next str -> reducing p(firstname) by factor {self.prefix_faktor}')
                logger.debug(f'        {sent}')
            else:
                pass
                                    
            ## position prefix: at the end
            if sent[-1][1] == 'prefix':
                if sent[-1][1] == 'prefix':
                    self.name['prefix'] = [sent[-1][0]]
                    sent = sent[:-1]
                    flag_prefix_end = True
                    logger.debug('        last word is prefix -> remove')
                    logger.debug(f'        {sent}')
                else: 
                    pass
            else:
                pass
                
        else:
            logger.debug('    no prefix found')
        
        
        
        ## concat prefix with the next str, if prefix is not at then end
#        while 'prefix' in [x[1] for x in sent[:-1]]:
#            ## wo ist der prefix?
#            idx = [x[1] for x in sent[:-1]].index('prefix')
#            sent[idx][1]=None
#            sent[idx+1][0]=sent[idx][0]+'_'+sent[idx+1][0]
#            ## prefix is more likely with lastname
#            sent[idx+1][2]=sent[idx+1][2]*self.prefix_faktor   # reduce p firstname
#            sent[idx+1][3]=1-sent[idx+1][2]     # adopt to p lastname
#        sent=[x for x in sent if x[1] != None]
#        logger.debug(f'    concat prefix with the next str -> reducing p(firstname) by factor {self.prefix_faktor}')
#        logger.debug(f'        {sent}')
        
        ## prefix at the end
#        if sent[-1][1] == 'prefix':
#            self.name['prefix'] = sent[-1][0]
#            self.sent = self.sent[:-1]
#            self.flag_prefix_end = True
#            logger.debug('    last word is prefix -> remove')
#            logger.debug(f'        {sent}')
#        else: 
#            self.flag_prefix_end = False
        
        
        if len(sent) == 1:
            sent[0][4]='last'
            logger.debug('    only one name -> last name')

 
        ## mark initials as FIRST
        sent=[  [x[0],x[1],x[2],x[3],'first'] if x[1]=='initial'\
                else x\
                for x in sent ]
        logger.debug('    initials are per definition first names')
        logger.debug(f'        {sent}')

                
        ## initials inside
        try:
            li=[x[1] for x in sent]
            cutidx = len(li) - 1 - li[::-1].index('initial')
        except:
            cutidx = -1

        if cutidx == -1:  
            logger.debug('    no initials inside')
            pass
        elif cutidx == 0:
            logger.debug('    initial at first position -> last word is last name')
            sent[-1][4]='last'
            logger.debug(f'        {sent}')
            #one = [ [x[0],x[1],x[2],x[3],'last'] for x in sent[1:]   ]
            #sent = [sent[0]]+one
            #logger.debug('    initial at first position -> all other words last name')
            #logger.debug(f'        {sent}')
        elif cutidx == len(sent)-1:
            sent[0][4]='last'
            logger.debug('    initial at last position -> first word is last name')
            logger.debug(f'        {sent}')
        else:
            if self.komma_inside:
                logger.debug('    comma inside -> do nothing') 
                logger.debug(f'        {sent}')
            else:
                one = [ [x[0],x[1],x[2],x[3],'first'] for x in sent[:cutidx+1]   ]
                two = [ [x[0],x[1],x[2],x[3], 'last'] for x in sent[cutidx+1:]   ]
                sent=one+two
                logger.debug('    no comma inside: initial between first and last position: before last initial is first name, after last initial is last name') 
                logger.debug(f'        {sent}')
            
        ## correct p values for already known 
        sent = [ [x[0],x[1],1,0,x[4]] if x[4]=='first' else x for x in sent ]
        sent = [ [x[0],x[1],0,1,x[4]] if x[4]=='last'  else x for x in sent ]
        logger.debug('    adjust p values for well defined first and last names')
        logger.debug(f'        {sent}')
        
        
        ## remove komma
        sent =[ x for x in sent if x[1] != 'komma']
        logger.debug('    komma removed')
        logger.debug(f'        {sent}')
        
        # any words not assigned?
        if None in [x[4] for x in sent]:
            not_assigned = True
        else:
            not_assigned = False

        if not_assigned == False:
            logger.debug('    all words are assigned')
            pass
        else:
            if sent[0][4]=='first' or sent[-1][4]=='last':
                directions=['fl']
            elif sent[0][4]=='last' or sent[-1][4]=='first':    
                directions=['lf']
            else:
                directions=['fl','lf']
            logger.debug(f'    order of names is: {directions}')
  
            #res_p=[]
            #max_p_total=[]
            p_total=[]    
            for direction in directions:
 
                if direction=='lf':
                    sent = sent[::-1]  

                for cut in range(1,len(sent)):
                    one = sent[:cut]
                    p_one = prod([x[2] for x in one])  # p for firstnames
                    two = sent[cut:]
                    p_two = prod([x[3] for x in two])  # p for lastnames
        
                    if direction=='lf':
                        one = one[::-1]  
                        two = two[::-1]  
            
                    p_total.append((direction,\
                                    cut,\
                                    p_one*p_two,\
                                    {'first':[x[0] for x in one],\
                                     'last':[x[0] for x in two]}\
                                    ))
    
                if direction=='lf':
                    sent = sent[::-1]  

        
                #max_p_total.append( [x  for x in p_total if x[2] == max([y[2] \
                 #                    for y in p_total])]  )
    
            result = [x for x in p_total if x[2] == max([y[2] for y in p_total]) ]
            
            logger.debug('    checked all possible cut off positions')
            
            
            sent = [ [x[0],x[1],x[2],x[3],'first'] \
                     if x[0] in result[0][3]['first'] \
                     else x \
                     for x in sent]
            
            sent = [ [x[0],x[1],x[2],x[3],'last'] \
                     if x[0] in result[0][3]['last'] \
                     else x \
                     for x in sent]

            logger.debug('    result:')
            logger.debug(f'        {sent}')
            
            ## add the prefix to the first lastname if we've removed it before
            if flag_prefix_end:
                idx = [x[4] for x in sent].index('last')
                a=self.name['prefix'][0]+'_'+sent[idx][0]
                sent[idx][0] = a
                logger.debug('    add again the prefix to the lastname which was removed from the end')
                logger.debug(f'        {sent}')
            else:
                pass
            
            
  
            
        return sent     




