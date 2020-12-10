import personnamenorm 
import string
pnn=personnamenorm.namenorm(debug=True)


## add initials
for x in string.ascii_lowercase:
    pnn.p_firstname[x]=1
    pnn.p_firstname[x+'.']=1
pnn.p_firstname['jr'] = 1
pnn.p_firstname['jr.'] = 1




## adding p values to the dict for this tests
pnn.p_firstname['first']=1
pnn.p_firstname['second']=1
pnn.p_firstname['third']=1
pnn.p_firstname['last']=1e-4
pnn.p_firstname['last2']=1e-4

#pnn.unify('Martin Roland '.lower())
#pnn.unify('MartinBettina '.lower())
#pnn.unify('Dr. von  und zu Förstner-Schmidt Konrad Ulrich  h. (MBA)')
#pnn.unify('Dr. Last')
#pnn.unify('Dr. Last-Last2')
#pnn.unify('Dr. Konrad U. Förstner (MBA)'.lower())
#print(pnn._get_p_word('konrad'))
#pnn.unify('Herrmann-Krotz Gabrielle')
#pnn.unify('Mueller Anna-Maria Markus')
#pnn.unify('FirstLast')
#pnn.unify('first von und zu last')
#pnn.unify('first ! § $ % & / \\ = ? * + # - _ . : ; < > | last')

#pnn.unify('Johannes Cornelis PAS VAN DE')
#pnn.unify('Friso Bernard Jan ASSEMA von')
#pnn.unify('Friso Bernard Jan von ASSEMA')
#pnn.unify('JUSTA MACNEIL Stacey Ann')
#pnn.unify('Stacey Ann JUSTA MACNEIL')
#pnn.unify('Celine SAVARIAR HAUCK')	                                 
#pnn.unify('VAN KOPPENHAGEN Juanita E')
#pnn.unify('Juanita E. VAN KOPPENHAGEN')
#pnn.unify('Ronald B. Fisher')
#pnn.unify('Valentino K. Stella')	                            #Stella, Valentino K
#pnn.unify('Robert P. Kimberly')
#pnn.unify('Nelson S. Yew')
#pnn.unify('Jonn Stefan')
#pnn.unify('Charles E. Jr. Davis')
#pnn.unify('G. Rodney Jr. Nelson')
pnn.unify('M. Victor Wickerhauser')
#pnn.unify('J. Richard Gyory')



#an initial must not be the first one in the list of firstnames !   REMOVE DOTS AFTER TITLE EXTRACTION !


from pprint import pprint
pprint(pnn.name)
