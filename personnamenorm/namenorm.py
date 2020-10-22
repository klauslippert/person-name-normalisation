from ftfy import fix_text
from nltk import word_tokenize as wt
import logging




# logging
logger = logging.getLogger(__name__)


class namenorm():
    '''
    unifying different notations of person names
    '''
    
    def __init__ (self,raw,debug=False):
        ''' 2DO      # to lower case in the beginning
                     # remove et.al
                     # remove underscore in prefix in the end
                     # strings mit nur zahlen -> allwords[-1] klappt nicht
        '''

        # handle logging: there is already logging
        if logger.hasHandlers():
            logger.addHandler(logging.NullHandler())
        # handle logging: no logging until now
        else:
            ch=logging.StreamHandler()
            ch.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s') )
            logger.addHandler(ch)

        #set log level for this module
        if debug:   
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        # create empty results
        self.name={
                   'raw':raw,
                   'firstname':[],
                   'lastname':[],
                   'title':[]
                  }
        self.fullname = ''
        self.fullname_abbrev = ''

        # check type of input
        if isinstance(raw,str) == False:
            logger.critical("Input must be <class 'str'>, you gave me "+str(type(raw)))
            return




        
        # general preparations
        _ = self._create_dict_lookup()
        
        # text preparations and extractions
        self.__text = self.name['raw'].strip()
        _ = self._fix_unicode()
        _ = self._remove_formating_chars()
        _ = self._remove_special_characters()
        _ = self._transform_prefixes()
        _ = self._tokenize_annotate()
        _ = self._extract_title()
        _ = self._remove_bracket_content()
        _ = self._tokenize_annotate()
        _ = self._extract_name()
        _ = self._extract_prefix()
        _ = self._capitalize()
        _ = self._create_output()
        

        
        if debug:
            logger.debug('annotation dict' + str(self.__sent))



    def _fix_unicode(self):    
        ''' fix bad unicode with ftfy 
            https://pypi.org/project/ftfy/
            
            in:  self.text <str> | text            
            out: self.text <str> | clean unicode text
        '''
        self.__text = fix_text(self.__text)

    def _remove_formating_chars(self):
        ''' remove 
            * tabs \t
            * everything which comes after newline \n or ¶
            
            in:  self.text  <str> | text
            out: self.text  <str> | text without formating chars
        '''
        self.__text = self.__text.replace('\n','CUT')
        self.__text = self.__text.replace('¶','CUT')
        self.__text = self.__text.split('CUT')[0].strip()
#        self.__text = self.__text.split('¶')[0].strip()
        #self.__text = ' '.join(self.__text.replace('\\t','').split())
        self.__text = self.__text.replace('\t',' ')    



    def _remove_special_characters(self):
       ''' remove special characters
   
            in:  self.text  <str> | text
            out: self.text  <str> | text without special chars       
       '''
       special_chars='!§%&/=<>;:-_$?*+#|'
       for char in special_chars:
           self.__text=self.__text.replace(char,' ')
       very_special_chars='\\'
       for char in very_special_chars:        
           self.__text=self.__text.replace(char,' ')
       
       self.__text=self.__text.replace("d'","d_ ")


    def _tokenize_annotate(self):
        ''' tokenize text (using nltk tokenizer)
            and annotate text (using lookup dict) 
        
            in:  self.text           <str> | text
                 self.dict_allg     <dict> | lookup dictionary
            out: self.sentence <list(str)> | tokenized text
                 self.annotate <list(str)> | annotations
        '''
        self.__sentence=wt(self.__text)
        self.__annotate=[]
        for word in self.__sentence:
            if word.isnumeric():
                self.__annotate.append('zahl')
            else:
                try:
                    self.__annotate.append(self.__dict_allg[word])
                except:
                    self.__annotate.append('str')

        self.__sent = [(x,y) for x, y in   zip(self.__sentence,self.__annotate )]

    def _create_dict_lookup(self):
        ''' lookup dictionaries for extracting 
            punctuations, titles, prefixes
            
            in:  None
            out: self.dict_allg  <dict> |  one lookup dictionary
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
                      'PhD', 'Ph.D.', 'Dr.',
                      'MBA','MSc.','BSc.','M.A.','B.A.',
                      'MSc','BSc','M.A','B.A',
                      'Dipl.','Dipl',
                      'Dipl.Ing.','Dr.Ing.','Dipl.Ing','Dr.Ing']

        dict_title = dict(zip(list_title, ['titel']*len(list_title)))

        # name prefixes
        prefix_list = ['von und zu','von dem','von der','von',    #german
                             'zu','vom','zum', 'van der',                         #german
                             'de',"d_",                                 #french
                             'di','de','del','da','degli','dalla',      #italian
                             'van de','van ter','van','ter'             #dutch
                                                                        #spanish MISSING
                                                                        #portuguese MISSING
                            ]
        
        prefix_list_sort = sorted(prefix_list,key=len,reverse=False)
        prefix_list_space = [' '+x+' ' for x in prefix_list_sort]
        prefix_list_underscore = ['_'.join(x.split()) for x in prefix_list_space]
        
        self.__prefix_list_space = prefix_list_space
        self.__prefix_list_underscore = prefix_list_underscore
        
        dict_prefix = dict(zip(prefix_list_underscore, ['prefix']*len(prefix_list_underscore)))

        _ = dict_allg.update(dict_title)
        _ = dict_allg.update(dict_prefix)
    
        self.__dict_allg = dict_allg
        logger.debug('annotation dict' + str(self.__dict_allg))
        
    def _remove_bracket_content(self):
        '''remove anything inside any brackets
           2do: keep titles inside brackets
           
           in:  self.sentence <list(str)> | tokenized text
                self.annotate <list(str)> | annotations
           out: self.sentence <list(str)> | tokenized text without brackets and content
                self.annotate <list(str)> | annotations without brackets and content
        '''
        while 1==1:
            try:
                von = self.__annotate.index('klammerauf')
                bis = self.__annotate.index('klammerzu')
                self.__annotate[von:bis+1]=''
                self.__sentence[von:bis+1]=''
            except:
                break
        
    def _transform_prefixes(self):
        ''' transforms prefixes in text
            for extracting them correctly
            by replacing spaces with underscore
            
            in:  self.__prefix_list_space      <list(str)> | list of prefixes with spaces
            out: self.__prefix_list_underscore <list(str)> | list of prefixes with underscore
        '''
        for x,y in zip(self.__prefix_list_space, self.__prefix_list_underscore):
            self.__text=self.__text.replace(x,' '+y+' ')

    def _extract_title(self):   
        ''' extract the educational titles
            
            in:  self.__sentence    <list(str)> | tokenized string
                 self.__annotate    <list(str)> | annotations
            out: self.name['title'] <list(str)> 
        '''
        self.name['title'] = [x for x,y in zip(self.__sentence,self.__annotate) if y == 'titel']

    def _extract_prefix(self):   
        ''' extract the prefix
            
            in:  self.__sentence     <list(str)> | tokenized string
                 self.__annotate     <list(str)> | annotations
            out: self.name['prefix'] <list(str)>
        '''
        self.name['prefix'] = [x for x,y in zip(self.__sentence,self.__annotate) if y == 'prefix']   
        self.name['prefix'] = [x.replace('_',' ') for x in self.name['prefix']]
        try: 
            idx=self.name['prefix'].index('d ')
            self.name['prefix'][idx]="d'"
        except:
            pass



    def _extract_name(self):
        ''' extract the first and the last names
            
            in:  self.__sentence     <list(str)> | tokenized string
                 self.__annotate     <list(str)> | annotations
            out: first and last names
        '''
        ## the question is: is there a comma ?
        try:
            idx=self.__annotate.index('komma')
        except: 
            idx=-1

        ## gather first and last names (both plural)
        firstname= []
        lastname=[]

        ## case 1:  lastnames comma firstnames
        ######################################
        if idx>-1:    
            vorkomma_sentence = self.__sentence[:idx]
            vorkomma_annotate = self.__annotate[:idx]
            nachkomma_sentence = self.__sentence[idx+1:]
            nachkomma_annotate = self.__annotate[idx+1:]
    
            # extract lastnames -> before comma
            while 1==1:
                try:
                    idx2 = vorkomma_annotate.index('str')
                    lastname.append(vorkomma_sentence[idx2])
                    vorkomma_annotate[idx2]=''
                except:
                    break
                    
            # extract firstnames -> after comma
            while 1==1:
                try:
                    idx2 = nachkomma_annotate.index('str')
                    firstname.append(nachkomma_sentence[idx2])
                    nachkomma_annotate[idx2]=''
                except:
                    break
                
        ## case 2:  firstnames lastnames
        ## assumption: only ONE lastname
        ######################################
        else:   
            allwords=[x    for x,y in zip(self.__sentence,self.__annotate) if y=='str']
            lastname = [allwords[-1]]
            firstname = allwords[:-1]
    
    
        self.name['firstname'] = firstname
        self.name['lastname']  = lastname
    
    def _capitalize(self):
        ''' capitalize First and Lastnames
        
            in: self.name  <dict> | resulting dict  
            out: self.name <dict> | resulting dict
        '''
        self.name['firstname'] = [x.capitalize() for x in self.name['firstname']]
        self.name['lastname'] = [x.capitalize() for x in self.name['lastname']]
    
    
    def _create_output(self):
        ''' create standardised output
            
            in:  self.name            <dict> | resulting dict
            out: standardised output
                 self.fullname:        <str> | (prefix) last, first .. not titles
                 self.fullname_abbrev: <str> | (prefix) last, initials .. not titles                 
        '''
        self.fullname = '{} {}, {}'.format(
                                           ' '.join(self.name['prefix']),
                                           ' '.join(self.name['lastname']),
                                           ' '.join(self.name['firstname'])
                                           )
        self.fullname_abbrev = '{} {}, {}'.format(
                                                  ' '.join(self.name['prefix']),
                                                  ' '.join(self.name['lastname']),
                                                  ' '.join([x[0] for x in self.name['firstname']])
                                                 )




     




